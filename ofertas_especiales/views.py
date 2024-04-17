from django.shortcuts import render
from utils.utils import cartData_especial
from correos.models import Correo
from envio.forms import UsuarioForm, EnvioForm, DecidirTarjetaForm
# Create your views here.


def cart_data(request):
    
    data = cartData_especial(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return cartItems, order, items


def ofertas_especiales_view(request):

    cartItems, order, items = cart_data(request)
    
    correos = Correo.objects.all()
    usuario_form = UsuarioForm(request.POST or None)
    envio_form = EnvioForm(request.POST or None)
    card_decidir_form = DecidirTarjetaForm(request.POST or None)
    print('ORDER:', order)
    print('ITEMS:', items)
    print('CARTITEMS:', cartItems)
    print('GET CART TOTAL:', order['get_cart_total'])
    
    context = {
                'items': items,
                'order': order, 
                'cartItems': cartItems,
                'correos':correos,
                'usuario_form':usuario_form,
                'envio_form':envio_form,
                'card_decidir_form': card_decidir_form,
                }

    return render(request, 'ofertas_especiales/ofertas_especiales.html', context)
    