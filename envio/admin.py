from django.contrib import admin
from .models import DatosEnvio
from compra.models import Compra
from cliente.models import Cliente
import requests
from processOrder.views import oca
from django.http import HttpResponseRedirect
import xml.etree.ElementTree 
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
import io
from xhtml2pdf import pisa 

class DatosEnvioAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {'fields':['fecha_added', 'cliente', 'compra', 'correo', 'numero_de_seguimiento', 'numero_de_retiro', 'etiqueta_impresa']}),
        ('Datos envio', {'fields':['direccion', 'ciudad', 'provincia', 'codigo_postal', 'telefono', 'indicaciones']})
    ]
    list_display = ['cliente', 'compra', 'fecha_added', 'correo']
    ordering = ['fecha_added']
    change_form_template = "envio/envio_changeform.html"

    def cancelar_envio(self, compra_nro_retiro):

        url = "http://webservice.oca.com.ar/epak_tracking/Oep_TrackEPak.asmx/AnularOrdenGenerada?usr=test@oca.com.ar&psw=123456&IdOrdenRetiro=%s" % (compra_nro_retiro)
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        decode_response = response.content.decode('utf-8')
        tree = xml.etree.ElementTree.fromstring(decode_response)
        print('DECODE RESPONSE:', response)

        respuesta = []
        codigo = []

        for child in tree:
            for k in child:
                for i in k:
                        for c in i:
                            if c.tag == 'Mensaje':
                                respuesta.append(c.text)
                            if c.tag == 'IdResult':
                                codigo.append(c.text)

        return respuesta, codigo


    def response_change(self, request, obj):

        form_datos_envios = request.POST
        compra = form_datos_envios['compra']
        datos_envio = DatosEnvio.objects.filter(compra__id=str(compra)).first()
        n_retiro = form_datos_envios['numero_de_retiro']

        if "ver-pdf" in request.POST:

            url = "http://webservice.oca.com.ar/epak_tracking/Oep_TrackEPak.asmx/GetDatosDeEtiquetasPorOrdenOrNumeroEnvio?idOrdenRetiro=%s&nroEnvio=%s&isLocker=%s" % (str(n_retiro) , '', 'False')
            payload={}
            headers = {}
            datos_etiqueta = {}
            products_list = []

            compra = Compra.objects.filter(id=str(compra)).first()

            for item in compra.get_cart_products:
                    products_list.append({item['quantity']:item['producto']['nombre_abreviado']})

            response_request = requests.request("GET", url, headers=headers, data=payload)
            response_decode = response_request.content.decode('utf-8')
            
            try:
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
        
                tf.seek(0)

                response = HttpResponse(tf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=etiquetas.pdf'
                return response

            except:
                return HttpResponse('No hay datos para esa etiqueta')
        
        elif "cambiar-etiqueta" in request.POST:

            respuesta, codigo = self.cancelar_envio(n_retiro)
            print('CODIGO:',codigo)
            print('RESPUESTA:', respuesta)
            print('COMPRA:', compra)

            try:
            
                if codigo[0] == '100' or codigo[0] == '130':
                    print("ENTRE")
                    customer = Cliente.objects.filter(email=compra.cliente).first()
                    print("CUSTOMER:", customer)
                    cartdata = {
                        'order':{'get_cart_total': compra.get_cart_total, 'get_cart_items': compra.get_cart_items, 'total_check':compra.total_check},
                        'items':compra.get_cart_products        
                    }

                    data = {
                            'shipping':{
                                'address':form_datos_envios['direccion'],
                                'city':form_datos_envios['ciudad'],
                                'state':form_datos_envios['provincia'],
                                'zipcode':form_datos_envios['codigo_postal'],
                                'directions':form_datos_envios['indicaciones']
                            },
                    }

                    nro_seguimiento, nro_retiro = oca(customer, data, cartdata)
                    print('NUMERO DE SEGUIMIENTO:', nro_seguimiento)
                    datos_envio.numero_de_seguimiento = nro_seguimiento
                    datos_envio.numero_de_retiro = nro_retiro
                    datos_envio.save()

                    self.message_user(request, "Etiqueta OCA creada o actualizada con exito")
                    print('ETIQUETA ENVIO ACTUALIZADA')
                    
                    return HttpResponseRedirect(".")
                    
                else:
                    self.message_user(request, respuesta[0], level=messages.WARNING)
                    return HttpResponseRedirect(".")

            except:

                self.message_user(request, "Ups algo salio mal, volve a intentar", level=messages.WARNING)
                return HttpResponseRedirect(".")


        elif "eliminar-etiqueta" in request.POST:
            respuesta, codigo = self.cancelar_envio(n_retiro)
            try:
            
                if codigo[0] == '100':
                    print('CODIGO 100')
                    self.message_user(request, "Etiqueta eliminada con exito")
                    return HttpResponseRedirect(".")
                
                else:
                    
                    self.message_user(request, respuesta[0], level=messages.WARNING)
                    return HttpResponseRedirect(".")

            except:

                self.message_user(request, "Ups algo salio mal, volve a intentar", level=messages.WARNING)
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)


    def get_queryset(self, request):

        qs = super().get_queryset(request)
        
        try:
            group = request.user.groups.all()[0].name
        except:
            group = None

        if group == 'CABA':
            return qs.filter(correo='CABA', compra__completada=False)
        elif group == 'BARILOCHE':
            return qs.filter(correo='BARILOCHE', compra__completada = False)
        else:
            return qs

      
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        
        print("render change form ", context.get('input'))
        print('OBJETO:', obj)

        if obj == None:                
            pass

        else:    

            if obj.correo == 'OCA':
                pass
            else:
                context.update({
                    'cambiar-etiqueta': False,
                    'eliminar-etiqueta': False,
                    'ver-pdf': False,
                    'show_Eliminar etiqueta': False,
                    'show_delete': False
                })

        return super().render_change_form(request, context, add, change, form_url, obj)

    
    def change_view(self, request, object_id=None, form_url='',extra_context=None):
        qs = DatosEnvio.objects.filter(id=object_id).first()
        print('obj_id:',qs.correo)
        is_super =  request.user.is_superuser

        if is_super == True and qs.correo == 'OCA':
           template_response = super().change_view(request, object_id, form_url,
                                                extra_context)
        else:
            # get the default template response
            template_response = super().change_view(request, object_id, form_url,
                                                extra_context)
            # here we simply hide the div that contains the save and delete buttons
            template_response.content = template_response.rendered_content.replace(
            '<div class="row-extra">',
            '<div class="row-extra" style="display: none">')
        return template_response


admin.site.register(DatosEnvio, DatosEnvioAdmin)


