from envio.models import DatosEnvio
from django.shortcuts import render, redirect
from django.http import JsonResponse
from compra.models import Compra
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from .charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from compra.models import Compra
from envio.models import DatosEnvio
import requests, json, io
import xml.etree.ElementTree 
from base64 import b64decode
from PyPDF2 import PdfFileMerger
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
from pyisemail import is_email
from decouple import config
from utils.utils import cartData


@user_passes_test(lambda u: u.is_superuser)
def get_filter_options(request):
    grouped_purchases = Compra.objects.annotate(year=ExtractYear('fecha_compra')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })


@staff_member_required
def get_sales_chart(request, year):
    purchases = Compra.objects.filter(fecha_compra__year=year)
    grouped_purchases = purchases.annotate(price=F('total')).annotate(month=ExtractMonth('fecha_compra'))\
        .values('month').annotate(average=Sum('total')).values('month', 'average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-1]] = round(group['average'], 2)
        

    return JsonResponse({
        'title': f'Ventas en {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Total ($)',
                'backgroundColor': '#F5EFC3',
                'borderColor': '#F5EFC3',
                'data': list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = Compra.objects.filter(fecha_compra__year=year)
    grouped_purchases = purchases.annotate(price=F('total')).annotate(month=ExtractMonth('fecha_compra'))\
        .values('month').annotate(average=Avg('total')).values('month', 'average').order_by('month')

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Promedio gasto por cliente en {year}',
        'data': {
            'labels': list(spend_per_customer_dict.keys()),
            'datasets': [{
                'label': 'Total ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(spend_per_customer_dict.values()),
            }]
        },
    })


@staff_member_required
def payment_success_chart(request, year):
    purchases = Compra.objects.filter(fecha_compra__year=year)

    return JsonResponse({
        'title': f'Compras concluidas {year}',
        'data': {
            'labels': ['Satisfactorias', 'No Satisfactorias'],
            'datasets': [{
                'label': 'Total ($)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': [
                    purchases.filter(completada=True).count(),
                    purchases.filter(completada=False).count(),
                ],
            }]
        },
    })


@staff_member_required
def payment_method_chart(request, year):
    purchases = Compra.objects.filter(fecha_compra__year=year)
    grouped_purchases = purchases.values('medio_de_pago').annotate(count=Count('id'))\
        .values('medio_de_pago', 'count').order_by('medio_de_pago')

    payment_method_dict = dict()
    m_d_pago = [('DECIDIR', 'DECIDIR'),('MERCADOPAGO', 'MERCADOPAGO')]

    for payment_method in m_d_pago:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        if group['medio_de_pago'] != None:
            #print('GROUP:', group['medio_de_pago'])
            payment_method_dict[dict(m_d_pago)[group['medio_de_pago']]] = group['count']
        else:
            pass

    return JsonResponse({
        'title': f'Medios de pago utilizados en {year}',
        'data': {
            'labels': list(payment_method_dict.keys()),
            'datasets': [{
                'label': 'Total ($)',
                'backgroundColor': generate_color_palette(len(payment_method_dict)),
                'borderColor': generate_color_palette(len(payment_method_dict)),
                'data': list(payment_method_dict.values()),
            }]
        },
    })


@staff_member_required
def mail_method_chart(request, year):
    purchases = DatosEnvio.objects.filter(fecha_added__year=year)
    grouped_purchases = purchases.values('correo').annotate(count=Count('id'))\
        .values('correo', 'count').order_by('correo')

    payment_method_dict = dict()
    correos = [('OCA', 'OCA'),('CABA', 'CABA'), ('BARILOCHE', 'BARILOCHE')]

    for payment_method in correos:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(correos)[group['correo']]] = group['count']

    return JsonResponse({
        'title': f'Correos utilizados {year}',
        'data': {
            'labels': list(payment_method_dict.keys()),
            'datasets': [{
                'label': 'Total ($)',
                'backgroundColor': generate_color_palette(len(payment_method_dict)),
                'borderColor': generate_color_palette(len(payment_method_dict)),
                'data': list(payment_method_dict.values()),
            }]
        },
    })


@staff_member_required
def statistics_view(request):
    return render(request, 'utils/statistics.html', {})



@staff_member_required
def etiquetas_view(request):

    filtered_datos_envio = DatosEnvio.objects.filter(Q(compra__status='PREPARANDO ORDEN')).\
                            exclude(Q(numero_de_seguimiento=1) | Q(numero_de_seguimiento=0)\
                            | Q(etiqueta_impresa=True)).order_by('-fecha_added').all()
    
    if request.method == 'GET':

        context = {
            'cantidad_compras':filtered_datos_envio.count(),
        }
        
        return render(request, 'utils/etiquetas.html', context)

    else:

        if request.POST.get("ver", "") == 'VER ETIQUETA/S':
            
            print('ENTRANDO A VER ETIQUETAS POR CANTIDAD')

            try:

                merger = PdfFileMerger()

                for envio in filtered_datos_envio:
                    products_list = []
                    print("NUMERO DE RETIRO:", envio.numero_de_retiro)

                    for item in envio.compra.get_cart_products:
                        products_list.append({item['quantity']:item['producto']['nombre_abreviado']})

                    url = "http://webservice.oca.com.ar/epak_tracking/Oep_TrackEPak.asmx/GetDatosDeEtiquetasPorOrdenOrNumeroEnvio?idOrdenRetiro=%s&nroEnvio=%s&isLocker=%s" % (str(envio.numero_de_retiro) , '', 'False')
                    payload={}
                    headers = {}
                    datos_etiqueta = {}

                    response_request = requests.request("GET", url, headers=headers, data=payload)
                    response_decode = response_request.content.decode('utf-8')
            
                    tree = xml.etree.ElementTree.fromstring(response_decode)
                    
                    for child in tree:
                        for k in child:
                    
                            tag = k.tag.replace('{#Oca_e_Pak}', '')
                            datos_etiqueta[tag]= k.text

                    template_path = 'utils/pdf_etiquetas.html'
                    context = {
                        'datos_etiqueta': datos_etiqueta,
                        'products_list' : products_list
                        }
                    template = get_template(template_path)
                    html = template.render(context)
    
                    tf = io.BytesIO()
                    pisa.pisaDocument(
                        src=io.BytesIO(html.encode("UTF-8")),
                        dest=tf,
                        encoding='UTF-8'
                    )

                    merger.append(tf)
                    datos_etiqueta = {}

                temp_file = io.BytesIO()
                merger.write(temp_file)
                temp_file.seek(0)
                
                response = HttpResponse(temp_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=etiquetas.pdf'
                return response
            except:
                return HttpResponse('No hay datos para esa etiqueta')
                       
 
        if request.POST.get("borrar", "") == 'MARCAR COMO IMPRESAS':
            
            print('CAMBIANDO ETIQUETAS A IMPRESAS TRUE')
            
            for etiqueta in filtered_datos_envio:
                etiqueta.etiqueta_impresa = True
                etiqueta.save()
            
            return redirect('etiquetas')


def email_validador(request):
    data_json = json.loads(request.body)
    captcha_value = data_json['captcha']
    #detailed_result_with_dns = is_email(data_json['email'], check_dns=True, diagnose=True)
    bool_result_with_dns = is_email(data_json['email_checkout'], check_dns=True)
    result_captcha = captcha_validador(captcha_value)
    print('resultado captcha', result_captcha)
    print('bool', bool_result_with_dns)
    print('EMAIL:', data_json['email_checkout'])

    if result_captcha['success'] == True:

        data = [{
                'email':bool_result_with_dns
            }]
    
    else:

        data = [{
                'email':'robot'
            }]

    return JsonResponse(data, safe=False)


def captcha_validador(captcha_value):

    data = {
        'response': captcha_value,
        'secret': config('SECRET_KEY_CAPTCHA')
    }

    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()

    return result_json


def update_slider(request):

    try:
        data = cartData(request)
        order = data['order']
        total =  order['total_check']
        print('total update slider:', total)
        if total == 0:
            t = '0'
        elif total >= 9000:
            t = 'mayor'
        else:
            t = 'menor'

        data = {
            'total':t,  
        }

    except:
         data = {
            'total':'error',  
        }

    return JsonResponse(data, safe=False)

