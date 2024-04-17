from django.shortcuts import render, get_object_or_404
from .models import Producto, ImagenesProducto, ItemsCombo
from correos.models import Correo
from utils.utils import cartData
from django.db.models import Q
import csv
from envio.models import Provincias, Localidad


def productos_view(request):
  
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    accesorios = Producto.objects.exclude(Q(sku='CB001') | Q(sku='CB016') | Q(combo=True)).order_by('-precio').all()
    combos = Producto.objects.filter(combo=True).order_by('-precio').all()
    planchettas = Producto.objects.filter(Q(sku='CB001') | Q(sku='CB016') | Q(sku='CB135')).order_by('-precio').all()
    
    products_sku = []
    for x in items:
        products_sku.append(x['producto']['sku'])

    print('PRODUCTS NAME:', products_sku)

    context = {
                'accesorios':accesorios, 
                'cartItems':cartItems,
                'order':order,
                'products_sku':products_sku,
                'combos':combos,
                'planchettas':planchettas
                }

    return render(request, 'productos/productos.html', context)


def detail_view(request, slug):

    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems'] 
    items = data['items']
    producto = get_object_or_404(Producto, slug=slug)
    photos = ImagenesProducto.objects.filter(post=producto)
    productos = Producto.objects.order_by('-precio').all()
    items_combo_query = ItemsCombo.objects.filter(productos__slug=slug)

    items_combo = []

    for item in items_combo_query:

        items_combo.append({
            'nombre':str(item.get_items_combo['items']['nombre']),
            'cantidad': item.get_items_combo['items']['cantidad']
            })

    print('ITEMS COMBO:', items_combo)
    print('CARACTERISTICA:', producto.caracteristicas)
    
    caracteristicas_lista = producto.caracteristicas.split('.')
    products_sku = []
    for x in items:
        products_sku.append(x['producto']['sku'])


    
    context = {
                'cartItems':cartItems,
                'order':order,
                'photos':photos,
                'producto':producto,
                'products':productos,
                'products_sku':products_sku,
                'caracteristicas_lista':caracteristicas_lista,
                'items_combo':items_combo
                }
                
    return render(request, 'productos/detail.html', context)






            