from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from compra.models import Compra
from utils.utils import cartData
from correos.models import Correo
from cliente.models import Cliente
from processOrder.views import envio_email, process_order_cash, processOrder, oca, tango
from decouple import config
from utils.views import payment_method_chart
from .models import DatosEnvio, Localidad
from time import time
import json, requests, datetime, mercadopago, math
from django.db.models import Q
from .forms import UsuarioForm, EnvioForm, DecidirTarjetaForm


data_user_shipping = {}
total = 0
r = ''
precio_correo = 0
porcentaje = 0


def checkout_view(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    usuario_form = UsuarioForm(request.POST or None)
    envio_form = EnvioForm(request.POST or None)
    card_decidir_form = DecidirTarjetaForm(request.POST or None)
    correos = Correo.objects.all()

    print('----checkout_view----')
    print('ITEMS:', items)
    print('get cart total', order)
    products_sku = []
    for x in items:
        products_sku.append(x['producto']['sku'])

    intereses = i= {
        '12':18.18,
        '18':28.84,
        '24':35.83
    }


    context = {
                'items': items, 
                'order': order, 
                'cartItems': cartItems,
                'products_sku':products_sku,
                'usuario_form':usuario_form,
                'envio_form':envio_form,
                'card_decidir_form': card_decidir_form,
                'recaptcha_site_key': config('SECRET_SITE_KEY'),
                'intereses': intereses,
                'correos': correos
                }
    
    
    return render(request, 'envio/envio.html', context)


def percentage(p, total):
    #print('percentage:', (int(p)*float(total)) / 100)
    return (int(p)*float(total)) / 100


def round_up(n):
    #print('NUMER:', n)
    #print('round up:', math.ceil(n * 1) / 1)
    return math.ceil(n * 1) / 1


def interest(data_json):
    
    if int(data_json['installments']) == 1 or int(data_json['installments']) == 3 or int(data_json['installments']) == 6:
        total_interest = total
    elif int(data_json['installments']) == 12:
        total_interest = ((float(total) * 18.18) / 100) + float(total) 
    elif int(data_json['installments']) == 18:
        total_interest = ((float(total) * 28.84) / 100) + float(total)
    elif int(data_json['installments']) == 24:
        total_interest = ((float(total) * 35.83) / 100) + float(total)
    else:
        total_interest = 'Error'

    #print('interest:', float(total_interest))

    return float(total_interest)


def correoYtotal(data_json, order, items):
    
    global total, precio_correo, porcentaje
    print("ENTRANDO A FUNCION correoYtotal")
    #print("order['get_cart_total']:", order['get_cart_total'])

    sum_total = float(order['total_check']) + float(order['total_check_especial'])
    #print('sum total:', sum_total)

    if sum_total < 4000:    
        print('Menor de 4000')  
        correo_p = Correo.objects.filter(nombre=data_json['shipping_info']['correo']).values()
        precio_correo = correo_p[0]['precio']
        total = float(order['get_cart_total']) + float(precio_correo)

    elif sum_total >= 4000 and sum_total < 9000: 
        print('Mayor 4000 y menor 9000')
        precio_correo = 0
        total = float(order['get_cart_total'])

    elif sum_total >= 9000:
        print('Mayor a 9000')
        porcentaje = percentage(10, float(order['total_check']))
        precio_correo = 0
        total = float(order['get_cart_total'])
        
    #elif order['total_check'] >= 10000 :
        #porcentaje = percentage(15, float(order['total_check']))
        #precio_correo = 0
        #total = float(order['get_cart_total'])


def cart_data(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return cartItems, order, items  


def create_preference(request):

    '''
        Crea la preferencia de MP
        y la retorna en un JsonResponse.
    '''
    try: 
        global data_user_shipping, r
        r = request
        print('REQUEST:', r.COOKIES['cart'])
        cartItems, order, items = cart_data(request)
        print('ORDER:', order)
        sdk = mercadopago.SDK(config('MP_KEY'))
        data_json = json.loads(request.body)
        
        print('CREATE PREFERENCE:', data_json)
        print('nombre:', data_json['user_info']['name'] )

        data_user_shipping = data_json

        print('DATA USER', data_json)

        correoYtotal(data_json, order, items)

        preference_data = {
            "items": [
                {
                    "title": 'IDACOM',
                    "quantity": 1,
                    "unit_price": total,
                }
            ],
            "back_urls": {
            "success": "https:///carrito?success",
            "failure": "https:///carrito?failure",
            "pending": "https:///carrito?pending"
            }, 
            "tracks": [
                {
                    "type": "facebook_ad",
                    "values": {
                        "pixel_id": ""
                    }
                },
                {
                "type": "google_ad",
                "values": {
                    "conversion_id": "",
                    "conversion_label": ""
                    }
                }
            ],
            "payment_methods": {
                "excluded_payment_types": [
                    {
                        "id": "credit_card"
                    },
                    {
                        "id": "debit_card"
                    }
                ],
            },
            "statement_descriptor": "IDACOM",
            "auto_return": "approved",     
            
        }   

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
       
        print(preference)

    except:
        
        preference = 'error'

    return JsonResponse(preference, safe=False)    


def decidir(request):

    '''
        PRISMA DECIDIR:
        Recibe los datos de tarjeta de credito/debito, 
        los valida, si son correctos, llama a processOrder()
        y retorna un JsonResponse con status aprovado,
        de lo contrario, no llama a processOrder() y
        retorna un JsonResponse con status error.
    '''
    try:
        data_json = json.loads(request.body)
        cartItems, order, items = cart_data(request)

        print('DECIDIR BACKEND BEGIN:', data_json)
        
        try:
            
            correoYtotal(data_json, order, items)
            total_interest = interest(data_json)
            url = "https://developers.decidir.com/api/v2/payments"

            payload = {
                "site_transaction_id":str('' + str(int(time()))),
                "token":data_json['result']['id'],
                "payment_method_id":1,
                "bin":data_json['result']['bin'],
                "amount":int(round_up(total_interest)),
                "currency":"ARS",
                "installments":int(data_json['installments']),
                "payment_type":'single',
                "sub_payments":[],
                "establishment_name":''         
            }

            headers = {
                'apikey': config("API_DECIDIR"),
                'content-type': "application/json",
            }

            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            response_json = response.json()
            print('RESPONSE:', response_json)

            try:
               
                status = response_json['status']

                if status == 'approved':
                    
                    url_deb_cre= "https://lookup.binlist.net/%s" % response_json['bin']
                    response_deb_cre = requests.request("GET", url_deb_cre)
                    response_deb_cre_json = response_deb_cre.json()
                    print('credito o debito:', response_deb_cre_json)

                    try:
                        deb_cre = response_deb_cre_json['type']
                    except:
                        deb_cre = 'credit'

                    data = {
                        'form': data_json['user_info'],
                        'shipping': data_json['shipping_info'],
                        'transaction_id':response_json['id'],
                        'total': float(total_interest),
                        'precio_correo':precio_correo,
                        'cuotas':int(data_json['installments']),
                        'date':str(response_json['date']).split('.')[0],
                        'cuota_total':float(float(total_interest) / int(data_json['installments'])),
                        #'cuota_total':str(data_json['transaction_details']['total_paid_amount']),
                        'dni_cuit':data_json['dni_cuit'],
                        'medio_pago':'DECIDIR',
                        #'provincia_nombre':data_json['provincia_nombre'],
                        'porcentaje': porcentaje,
                        'card_brand': str(response_json['card_brand']).upper(),
                        'credito_debito': deb_cre
                    }

                    processOrder(request, data)

                    return JsonResponse(status, safe=False)
                
                else:
                    return JsonResponse(status, safe=False)

            except:
                
                if response_json['error_type'] == 'invalid_request_error':
                    return JsonResponse('Verifica los datos de la tarjeta y volve a intentar.', safe=False)
        
        except:

            print('DATA_JSON', data_json['result'])
            if data_json['result']['error_type'] == 'invalid_request_error':
                return JsonResponse('Verifica los datos de la tarjeta y volve a intentar.', safe=False)

    except:
        
        status = 'error'
        return JsonResponse(status, safe=False)


def email_verification(request):

    '''
        Verifica si el email del cliente esta registrado
        como usuario en la db.
        Retorna un JsonResponse con true/false.
    '''
    try:

        data_json = json.loads(request.body)
        query = Cliente.objects.filter(email=data_json['email']).exists()
    
        data = [{
            'cliente':query
        }]
    
    except:

        data = [{
            'cliente':'error'
        }]

    return JsonResponse(data, safe=False)


def address_finder(request):

    '''
        Verifica ciudad y provincia en la db, y 
        retorna un JsonResponse con el codigo postal.
    '''
    data_json = json.loads(request.body)
    city = data_json['city']
    state = data_json['state']
    
    print("PROVINCIA:", state)

    normalMap = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
             'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
             'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
             'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
             'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
             'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
             'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
             'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
             'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
             'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
             'Ñ': 'N', 'ñ': 'n',
             'Ç': 'C', 'ç': 'c',
             '§': 'S',  '³': '3', '²': '2', '¹': '1'}
    normalize = str.maketrans(normalMap)

    print('CIUDAD:', city.translate(normalize))
    try:

        query = Localidad.objects.filter(Q(provincia_id__nombre=str(state.translate(normalize)).title()) & Q(nombre=str(city.translate(normalize)).upper())).values()
        #print("QUERY:",query[0]['codigo_postal'])

        zc  = query.first()
        zipcode = zc['codigo_postal']
       
        data = [{
            'zipcode':zipcode
        }]
    
    except:
        
        data = [{
            'zipcode':'none'
        }]

    return JsonResponse(data, safe=False)


@csrf_exempt
def notifications(request):

    '''
    
    Mercado Pago notification endpoint:

    1-  Pending: Guarda la orden en la db sin Tango y Oca. Llama a process_order_cash(). 
        Rapi Pago/Pago Facil, orden status: PENDIENTE.
    
    2-  Approved: 
            -a: Crea la etiqueta OCA y manda los datos de facturacion a Tango. LLama a tango() y oca().
                DB status orden status: PENDIENTE a PREPARANDO ORDEN.
            -b: Crea orden, etiqueta Oca y manda los datos de facturacion a Tango processOrder().
                Usuario MP: efectivo en la cuenta, tarjeta credito/debito. DB status orden status:PREPARANDO ORDEN.
    
    3- Responde a Mercado Pago webhook HttpResponse('Recibido', status=200).
    
    '''

    '''
        Private code
    '''
    
    pass


