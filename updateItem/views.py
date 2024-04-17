from django.shortcuts import render
from django.http import JsonResponse
import json
from productos.models import Producto
from compra.models import Compra, OrderItem
from utils.utils import cartData

def updateItem(request):

    cart_data = cartData(request)
    data = json.loads(request.body)
    productId =data['productId']
    quantity = data['quantity']
   
    print('product:', productId)
    print('QUANTITY:', quantity)

    customer = request.user.cliente
    product = Producto.objects.get(id=productId)
    order, created = Compra.objects.get_or_create(cliente=customer, status=None, completada=False)
    orderItem, created = OrderItem.objects.get_or_create(compra=order, producto=product) 
    
    if data['action'] == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif data['action'] == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif data['action']  == 'delete':
        orderItem.quantity = 0
    else:
        orderItem.quantity = quantity
        
    orderItem.save()

    if int(orderItem.quantity) <= 0:
        orderItem.delete()

    items = OrderItem.objects.filter(compra=order).count()

    data =[{
        'data':str(items)
    }]
   
    return JsonResponse(data, safe=False)

