from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponse
from compra.models import Compra
from envio.models import DatosEnvio
from utils.utils import cartData, guestOrder
from decimal import Decimal
from pathlib import Path
from email.mime.image import MIMEImage
import json
import requests
import xml.etree.ElementTree 
import random
import string
import datetime
import threading
import time
from datetime import datetime as dt
from multiprocessing import Process

def processOrder(request, data):

     '''
          Procesa la orden APROVADA que se envia de Prisma o MP.
          Guarda la orden, los datos de envio, manda datos de facturacion
          a la API de Tango, crea la etiqueta de OCA y manda email al cliente con
          datos de la compra.

     '''

     start = time.process_time()
     cartdata = cartData(request)
   
     if request.user.is_authenticated:

          customer = request.user.cliente
          order, created = Compra.objects.get_or_create(cliente=customer, status=None, completada=False)

     else:

          customer, order = guestOrder(request, data) 
     
     customer.dni_cuit = data['dni_cuit']
     customer.save()

     print('CUSTOMER:', customer)        
     print('ORDER GET CART TOTAL:',order.get_cart_total)
     print('TOTAL:', float(data['total']))
     
     if float(data['total']) >= float(order.get_cart_total):
         
          order.medio_de_pago = data['medio_pago']
          order.transaction_id = data['transaction_id']
          order.total = Decimal(data['total'])
          order.descuento = Decimal(data['porcentaje'])
          order.status = 'PREPARANDO ORDEN'
          order.fecha_compra = datetime.datetime.now(tz=timezone.utc)
          order.correo = data['shipping']['correo']
          order.save()

          if data['shipping']['correo'] == 'OCA':

               n_envio, n_retiro = oca(customer,data,cartdata)
               numero_seguimiento =n_envio    
               numero_retiro =n_retiro

          else:

               numero_retiro = 0

               if data['shipping']['correo'] == 'CABA':
                    numero_seguimiento = 1

               else:
                    numero_seguimiento = 2  

          datos_envio = DatosEnvio.objects.create(
               cliente=customer,
               compra=order,
               direccion=data['shipping']['address'].upper(),
               ciudad=data['shipping']['city'].upper(),
               provincia=data['shipping']['state'].upper(),
               codigo_postal=data['shipping']['zipcode'],
               telefono=customer.telefono,
               correo=data['shipping']['correo'],
               indicaciones=data['shipping']['directions'],
               numero_de_seguimiento = numero_seguimiento,
               numero_de_retiro = numero_retiro
          )

          tipo_pago = 'tarjeta'
          
          threading.Thread(target=tango(customer, data, cartdata, datos_envio.id, tipo_pago)).start()
          threading.Thread(target=envio_email(customer, order, data['shipping']['correo'], cartdata, datos_envio.numero_de_seguimiento)).start()

          #envio_email(customer, order.numero_de_seguimiento, data['shipping']['correo'])
          #tango(customer, data, cartdata, shipping_id )

          print('TIEMPO PROCESSORDER:', time.process_time() - start)
          
          return HttpResponse(status=200)


def tango(customer, data, cartdata, shipping_id, tipo_pago):

     '''
     Private code
     '''

     print('###################  ENTRANDO A FUNCION TANGO  ####################')

     order = cartdata['order']
     items = cartdata['items']
     total_order = float(order['get_cart_total'])  
     productos_nombres = [producto['producto']['nombre'] for producto in items]
     order_items = items_lista(order, items, productos_nombres)
     financial_surcharge = [0.0 if int(data['cuotas']) <= 6 else float(data['total']) - float(total_order)]
     categoria_iva = ["CF" if len(str(customer.dni_cuit)) < 9 else "RI"]
     documento_tipo = ['96' if categoria_iva == 'CF' else '80']
     prov_id = provincia_id(data['shipping']['state'].upper())

     print('ORDER:', order)
     print("TOTAL ORDER", total_order)
     print("CUOTA TOTAL", data['cuota_total'])
     print('TOTAL:', float(float(data['cuota_total']) * int(data['cuotas'])) )
     print('PAID TOTAL:', f"{float(float(data['cuota_total']) * int(data['cuotas'])):.2f}")
     print("PERCENTAGE:", data['porcentaje'])
     print('TOTAL CON INTERES o SIN:', data['total'] )
     print("PROVINCIA ID:", prov_id)
     print("Financial surcharge:", financial_surcharge[0])

     
     url = "https://tiendas.axoft.com/api/Aperture/order"

     headers = {
     'accesstoken': '',
     'Content-Type': 'application/json'
     }

     response = requests.request("POST", url, headers=headers, data=json.dumps(orden))

     print(response.text)
     print('###################  TERMINANDO FUNCION TANGO  ####################')

     return None


def oca(customer, data, cartdata):

     today = dt.today().date()
     print("TODAY:", today)
     print('customer email OCA:', customer.email)
     print('customer nombre  OCA:', customer.nombre)
     print('customer apellido OCA:', customer.apellido)
     print('Data Oca:', data)
    
     nombre = str(customer.nombre + ' ' + customer.apellido)
     url = "http://webservice.oca.com.ar/ePak_tracking_TEST/Oep_TrackEPak.asmx/IngresoORMultiplesRetiros?usr=test@oca.com.ar&psw=123456&xml_Datos=<ROWS><cabecera ver=\"2.0\" nrocuenta=\"1\" /><origenes><origen calle=\"\" nro=\"\" piso=\"\" depto=\"\" cp=\"7600\" localidad=\"MAR DEL PLATA\" provincia=\"BUENOS AIRES\" contacto=\" WhatsApp \" email=\o@g.com\" solicitante=\"\" observaciones=\"\" centrocosto=\"\" idfranjahoraria=\"1\" idcentroimposicionorigen=\"71\" fecha=\"%s\"><envios><envio idoperativa=\"64665\" nroremito=\"%s\"><destinatario apellido=\"%s\" nombre=\"%s\" calle=\"%s\" nro=\"\" piso=\"\" depto=\"\" localidad=\"%s\" provincia=\"%s\" cp=\"%s\" telefono=\"\" email=\"%s\" idci=\"0\" celular=\"%s\" observaciones=\"%s\" /><paquetes> <paquete alto=\"2.5\" ancho=\"28\" largo=\"48\" peso=\"3.5\" valor=\"1\" cant=\"1\" /></paquetes></envio></envios></origen></origenes></ROWS>&ConfirmarRetiro=True&DiasHastaRetiro=4&FranjaHoraria=1&ArchivoCliente=''&ArchivoProceso=''" % (today.strftime("%Y%m%d"), customer.dni_cuit, '', nombre, data['shipping']['address'].upper(), data['shipping']['city'].upper(), data['shipping']['state'].upper(), data['shipping']['zipcode'], customer.email, customer.telefono, data['shipping']['directions'].upper())

     payload={}
     headers = {}

     response = requests.request("GET", url, headers=headers, data=payload)
     x = response.content.decode('utf-8')
     print("RESPONSE OCA:", x)
     tree = xml.etree.ElementTree.fromstring(x)
     #xml.etree.ElementTree.dump(tree)  
     numero_envio = []
     orden_retiro = []
     
     for child in tree:
          for k in child:
               for i in k:
                    for c in i:
                         if c.tag == 'NumeroEnvio':
                              numero_envio.append(c.text)
                         if c.tag == 'OrdenRetiro':
                              orden_retiro.append(c.text)

     print('NUMERO DE ENVIO OCA:', numero_envio[0])
     print('NUMERO DE RETIRO OCA:', orden_retiro[0]) 

     return (numero_envio[0], orden_retiro[0])


def envio_email(customer, order, correo_nombre, cartdata, numero_seguimiento):
     
     items = cartdata['items']
     contra = ''.join(random.sample(string.ascii_lowercase, 10))
     ran_pass = make_password(contra)
     usuario = User.objects.filter(username=customer.email).exists()
     image_path = 'static/images/logo_idacom_email.png'
     image_logo = Path(image_path).name

     context = {
          'email_cliente': customer.email,
          'numero_envio': numero_seguimiento,
          'correo_nombre': correo_nombre,
          'contra': contra,
          'usuario': usuario,
          'items': items,
          'total': order.get_cart_total
     }

     template = get_template('enviar_email/email_compra.html')
     content = template.render(context)

     if usuario == False:
          user = User.objects.create(username=customer.email, first_name=customer.nombre, last_name=customer.apellido, email=customer.email, password=ran_pass)
          customer.user = user
          customer.save()  
    
     email = EmailMultiAlternatives(
          '',
          '',
          settings.EMAIL_HOST_USER,
          [customer.email,]
     )

     email.content_subtype = 'html'  # set the primary content to be text/html
     email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image 

     with open(image_path, mode='rb') as f:
          image = MIMEImage(f.read())
          email.attach(image)
          image.add_header('Content-ID', f"<{image_logo}>")

     email.attach_alternative(content, 'text/html')
     email.send()

     return None  

     

def process_order_cash(request, data):

     '''
          Procesa la orden que se envia de MP cuando es pago 
          en efectivo (RAPIPAGO/PAGO FACIL).
          Guarda la orden como PENDIENTE y los datos de envio.

     '''

     print('GUARDANDO ORDEN RAPIPAGO / PAGO FACIL')
     
     if request.user.is_authenticated:
          customer = request.user.cliente
          order, created = Compra.objects.get_or_create(cliente=customer, status=None, completada=False)   
     else:

          customer, order = guestOrder(request, data) 

     customer.dni_cuit = data['dni_cuit']
     customer.save()

     #print('CUSTOMER:', customer)        
     #print(order.get_cart_total)
     
     if float(data['total']) >= float(order.get_cart_total):
          
          order.completada = False
          order.medio_de_pago = data['medio_pago']
          order.transaction_id = data['transaction_id']
          order.total = Decimal(data['total'])
          order.descuento = Decimal(data['porcentaje'])
          order.status = 'PENDIENTE'    
          order.fecha_compra = datetime.datetime.now(tz=timezone.utc)
          order.correo = data['shipping']['correo']
          order.save()
     
          DatosEnvio.objects.create(
               cliente=customer,
               compra=order,
               direccion=data['shipping']['address'].upper(),
               ciudad=data['shipping']['city'].upper(),
               provincia=data['shipping']['state'].upper(),
               codigo_postal=data['shipping']['zipcode'],
               telefono=customer.telefono,
               correo=data['shipping']['correo'],
               indicaciones=data['shipping']['directions'],
          )

          contra = ''.join(random.sample(string.ascii_lowercase, 10))
          ran_pass = make_password(contra)

          usuario = User.objects.filter(username=customer.email).exists()

          if usuario == False:
               user = User.objects.create(username=customer.email, first_name=customer.nombre, last_name=customer.apellido, email=customer.email, password=ran_pass)
               customer.user = user
               customer.save()

     print('TERMINANDO RAPIPAGO / PAGO FACIL')

     return HttpResponse(status=200)


def items_lista(order, items, productos_nombres):

     order_items = []

     for producto in items:
          
          if order['get_cart_total'] == order['total_check'] or producto['producto']['precio_descuento'] == 0 :
               order_items.append(
                    {
                         "ProductCode": producto['producto']['id'],
                         "SKUCode": producto['producto']['sku'],
                         "VariantCode": " ",
                         "Description": producto['producto']['nombre'],
                         "VariantDescription": " ",
                         "Quantity": float(producto['quantity']),
                         "UnitPrice": float(producto['producto']['precio']),
                         "DiscountPercentage": 0.0
                    }
               )
          else:
               if 'LA PLANCHETTA® 2 HORNALLAS' in productos_nombres or 'LA PLANCHETTA® 1 HORNALLA' in productos_nombres:
                    order_items.append(
                         {
                              "ProductCode": producto['producto']['id'],
                              "SKUCode": producto['producto']['sku'],
                              "VariantCode": " ",
                              "Description": producto['producto']['nombre'],
                              "VariantDescription": " ",
                              "Quantity": float(producto['quantity']),
                              "UnitPrice": float(producto['producto']['precio_descuento']),
                              "DiscountPercentage": 0.0
                         }
                    )
               else:
                    order_items.append(
                         {
                              "ProductCode": producto['producto']['id'],
                              "SKUCode": producto['producto']['sku'],
                              "VariantCode": " ",
                              "Description": producto['producto']['nombre'],
                              "VariantDescription": " ",
                              "Quantity": float(producto['quantity']),
                              "UnitPrice": float(producto['producto']['precio']),
                              "DiscountPercentage": 0.0
                         }
                    )

     print("ORDER ITEMS:", order_items)

     return order_items 


def provincia_id(provincia_nombre):

     provincias_id = {
          'BUENOS AIRES': 1,
          'CATAMARCA': 2,
          'CORDOBA':3,
          'CORRIENTES':4,
          'ENTRE RIOS':5,
          'JUJUY':6,
          'MENDOZA':7,
          'LA RIOJA':8,
          'SALTA':9,
          'SAN JUAN':10,
          'SAN LUIS':11,
          'SANTA FE':12,
          'SANTIAGO DEL ESTERO':13,
          'TUCUMAN':14,
          'CHACO':16,
          'CHUBUT':17,
          'FORMOSA': 18,
          'MISIONES':19,
          'NEUQUEN':20,
          'LA PAMPA':21,
          'RIO NEGRO':22,
          'SANTA CRUZ':23,
          'TIERRA DEL FUEGO':24
     }

     provincia_Id = ''

     for key, value in provincias_id.items():
          if provincia_nombre == key:
               provincia_Id = str(value)

     return provincia_Id