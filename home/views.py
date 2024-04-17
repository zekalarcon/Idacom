from django.shortcuts import render
from utils.utils import cartData
from productos.models import Producto
# Suppress broken pipe errors
from django.core.servers.basehttp import WSGIServer
WSGIServer.handle_error = lambda *args, **kwargs: None


def home_view(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Producto.objects.filter(combo=False).order_by('-precio').all()
    combos = Producto.objects.filter(combo=True).order_by('-precio').all()
    productos_schema_org = Producto.objects.order_by('-precio').all()
    
    products_sku = []
    for x in items:
        products_sku.append(x['producto']['sku'])

    print("USUARIO:", request.user)
    
    context = {
        'items': items, 
        'order': order,
        'cartItems': cartItems,
        'products': products,
        'combos': combos,
        'products_sku':products_sku,
        'productos_schema_org':productos_schema_org,
        }

    return render(request, "home/home.html", context)

