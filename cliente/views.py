from django.shortcuts import render, redirect
from utils.utils import cartData
from .forms import PanelClienteForm
from django.contrib.auth.models import User
from .models import Cliente
from envio.models import DatosEnvio
import json
from django.http import JsonResponse
from productos.models import ProductosCalificacion, Producto
from compra.models import Compra
from django.db.models import Count, F, Sum, Avg

# Create your views here.

def panel_cliente_view(request):
    
    client_form = PanelClienteForm(request.POST or None)

    if request.method == "POST":

        if client_form.is_valid():
    
            nombre_cliente = client_form.cleaned_data['nombre'].upper()
            apellido_cliente = client_form.cleaned_data['apellido']
            telefono_cliente = client_form.cleaned_data['telefono']
            email_cliente   = client_form.cleaned_data['email']

            user = User.objects.get(username=request.user.cliente)
            cliente = Cliente.objects.get(user= user)

            user.username = email_cliente
            user.first_name = nombre_cliente
            user.last_name = apellido_cliente
            user.email = email_cliente
            cliente.nombre = nombre_cliente
            cliente.apellido = apellido_cliente
            cliente.telefono = telefono_cliente
            cliente.email = email_cliente
            user.save()
            cliente.save()

            return redirect('panelcliente')
    
    else:

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        query_pendiente = DatosEnvio.objects.filter(cliente=request.user.cliente, compra__status='PENDIENTE').all()
        query_preparando = DatosEnvio.objects.filter(cliente=request.user.cliente, compra__status='PREPARANDO ORDEN').all()
        query_encamino = DatosEnvio.objects.filter(cliente=request.user.cliente, compra__status='EN CAMINO').all()
        query_retiro = DatosEnvio.objects.filter(cliente=request.user.cliente, compra__status='LISTA PARA RETIRAR').all()
        query_entregado = DatosEnvio.objects.filter(cliente=request.user.cliente, compra__status='ENTREGADO').all()
        query_productos_calificaciones = ProductosCalificacion.objects.filter(cliente=request.user.id).all()
        query_count = DatosEnvio.objects.filter(cliente=request.user.cliente).count()
   
        
        compras_pendiente  = []
        compras_activas = []
        compras_entregado = []
        compras_calificaciones = {}

        for item in query_productos_calificaciones:
            if item.compra_id in compras_calificaciones:
                compras_calificaciones[item.compra_id].append({
                    'nombre':item.producto.nombre,
                    'calificacion':int(item.calificacion)
                })
            else:
                compras_calificaciones[item.compra_id] =[{
                    'nombre':item.producto.nombre,
                    'calificacion':int(item.calificacion)
                }]

        for item in query_pendiente:
            compras_pendiente.append((item.compra.get_cart_products, item.compra.status, item.compra.total, int(item.numero_de_seguimiento)))
               
        for item in query_preparando:
            compras_activas.append((item.compra.get_cart_products, item.compra.status, item.compra.total, int(item.numero_de_seguimiento)))

        for item in query_encamino:
            compras_activas.append((item.compra.get_cart_products, item.compra.status, item.compra.total, int(item.numero_de_seguimiento)))

        for item in query_retiro:
            compras_activas.append((item.compra.get_cart_products, item.compra.status, item.compra.total, int(item.numero_de_seguimiento)))

        for item in query_entregado:
            dic_productos = item.compra.get_cart_products
         
            if item.compra.id in compras_calificaciones:
                for producto in dic_productos:
                    for k,v in compras_calificaciones.items():
                        
                        for x in v:
                            if producto['producto']['nombre'] == x['nombre']:
                                producto['calificacion'] = x['calificacion']
                            
                compras_entregado.append((dic_productos, item.compra.status, item.compra.total, int(item.numero_de_seguimiento), int(item.compra.id)))

            else:

                dic_productos[0]['producto']['calificacion'] = 'sin calificar'

                compras_entregado.append((dic_productos, item.compra.status, item.compra.total, int(item.numero_de_seguimiento), int(item.compra.id)))

        client_form = PanelClienteForm(
                        initial={
                            'nombre': request.user.cliente.nombre,
                            'apellido':request.user.cliente.apellido,
                            'telefono':request.user.cliente.telefono,
                            'email':request.user.cliente.email
                            }
                        )

        context = {
                    'items': items, 
                    'order': order, 
                    'cartItems': cartItems,
                    'compras_pendiente': compras_pendiente,
                    'compras_activas':compras_activas,
                    'compras_entregado': compras_entregado,
                    'cliente_form': client_form,
                    'user': request.user,
                    'query_count': query_count
                }
                       
        return render(request, 'cliente/panelcliente.html', context)


def calificar_producto(request):

    data_json = json.loads(request.body)
    producto_id = data_json['producto_id']
    compra_id = data_json['compra_id']
    calificacion = data_json['calificacion']
    user =  Cliente.objects.get(user=request.user)
    producto = Producto.objects.filter(id=producto_id).first()
    producto_calificacion = ProductosCalificacion.objects.create(compra_id=compra_id, producto=producto, cliente=user, calificacion=calificacion)
    compra = Compra.objects.filter(id=compra_id).first()
    compra.calificacion = producto_calificacion
    compra.save()
    producto.update_calificacion

    data = [{
        'mensaje':'guardado'
    }]
    
    return JsonResponse(data, safe=False)



def eliminar_cuenta(request):

    data_json = json.loads(request.body)
    user = data_json['cliente']

    usuario = User.objects.filter(username=user).first()

    try:
        usuario.is_active = False
        usuario.save()

        data = [{
            'mensaje':'eliminado'
        }]
        
    except:

        data = [{
            'mensaje':'error'
        }]

    return JsonResponse(data, safe=False)
