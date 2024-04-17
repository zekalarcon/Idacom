from django.shortcuts import render
from productos.models import Producto
from utils.utils import cartData
from .forms import UsuarioForm, EnvioForm, DecidirTarjetaForm
from correos.models import Correo
from decouple import config

def carrito_view(request):
     
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Producto.objects.order_by('-precio').all()
    correos = Correo.objects.all()
    usuario_form = UsuarioForm(request.POST or None)
    envio_form = EnvioForm(request.POST or None)
    card_decidir_form = DecidirTarjetaForm(request.POST or None)

    print('----carrito_view----')
    print('ITEMS:', items)

    products_sku = []
    for x in items:
        products_sku.append(x['producto']['sku'])

    #print('PRODUCTS SKU:', products_sku)

    context = {
                'items': items, 
                'order': order, 
                'cartItems': cartItems,
                'products':products,
                'products_sku':products_sku,
                'correos':correos,
                'usuario_form':usuario_form,
                'envio_form':envio_form,
                'card_decidir_form': card_decidir_form,
                'recaptcha_site_key': config('SECRET_SITE_KEY')
                }
    
    
    return render(request, 'compra/compra.html', context)

    
    
