import json
from cliente.models import Cliente
from productos.models import Producto
from compra.models import Compra, OrderItem


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    items_sku = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'total_check': 0, 'total_check_especial': 0, 'shipping': False}
    cartItems = 0
    total = 0

    for item in cart:
        cartItems += cart[item]["quantity"]
        order['get_cart_items'] += cart[item]["quantity"]

    try:

        for i in cart:

            producto = Producto.objects.get(id=i)
            #order['total_check'] += (producto.precio * cart[i]["quantity"])
            
            item = {
                'producto': {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'nombre_abreviado':producto.nombre_abreviado,
                    'precio': producto.precio,
                    'precio_descuento': producto.precio_descuento,
                    'precio_tachado':producto.precio_tachado,
                    'imageURL': producto.imageURL,
                    'sku':producto.sku,
                    'slug':producto.slug,
                    'especial':producto.especial
                },
            'quantity': cart[i]['quantity'],
            'get_total': (producto.precio * cart[i]["quantity"]),
            'get_total_discounted': (producto.precio_descuento * cart[i]["quantity"])
            }

            items.append(item)
            items_sku.append(producto.sku)

        especial_total = 0

        for i in cart:

            producto = Producto.objects.get(id=i)
            #order['total_check'] += (producto.precio * cart[i]["quantity"])
            if producto.especial == True:
                especial_total += producto.precio * cart[i]["quantity"] 
            elif 'CB016' in items_sku and cartItems > 1:      
                total = sum([producto.precio * cart[i]["quantity"] if producto.precio_descuento == 0 else producto.precio_descuento * cart[i]["quantity"]])
                print('TOTAL CON PLANCHETTA 2:', total)
            elif 'CB016' in items_sku and cartItems == 1:
                total = (producto.precio * cart[i]["quantity"])  
                
            elif 'CB001' in items_sku and cartItems > 1:
                total = sum([producto.precio * cart[i]["quantity"] if producto.precio_descuento == 0 else producto.precio_descuento * cart[i]["quantity"]])
                
            elif 'CB001' in items_sku and cartItems == 1:
                total = (producto.precio * cart[i]["quantity"])  
                
            else:         
                total = (producto.precio * cart[i]["quantity"])   

            order['total_check'] += (total)
            order['get_cart_total'] += total

        print("TOTAL CHECK:",order['total_check'] )
        print('TOTALLLLLLL:', order['get_cart_total'])
        print('ESPECIAL:', especial_total)
        
        if float(order['get_cart_total']) >= 9000 or especial_total > 0:
            if float(order['get_cart_total']) == 0:
                total = especial_total
                print('especial')
            else:
                porcentaje = (int(10)*float(order['get_cart_total'])) / 100
                t = float(order['get_cart_total']) - porcentaje
                total = t + float(especial_total)
            print('TOTAL 10% OFF:', total )

        #elif float(order['get_cart_total']) >= 10000:
            #porcentaje = (int(15)*float(order['get_cart_total'])) / 100
            #total = float(order['get_cart_total']) - porcentaje
            #print('TOTAL 15% OFF:', total )

        else:
            total = order['get_cart_total'] + float(especial_total)

        order['get_cart_total'] = total  
        order['total_check_especial'] = especial_total

    except:
        pass
       
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.cliente
        order, created = Compra.objects.get_or_create(cliente=customer, status=None, completada=False)
        #items = order.orderitem_set.all()
        items = order.get_cart_products
        cartItems = order.get_cart_items
        order_dict = {'get_cart_total': order.get_cart_total, 'get_cart_items': order.get_cart_items, 'total_check':order.total_check, 'total_check_especial':order.total_check_especial }
        
        print('----cartData user authenticated----')
        print('order:',order_dict)
        print('items:',items)
        print('cartitems:', cartItems)
        print('----ITEMS inside items----')
        for x in items:
            print(x)
        
          
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order_dict = cookieData['order']
        items = cookieData['items']

        print('----cartData user Anonymous----')
        print('order:',order_dict)
        print('items:',items)
        print('cartitems:', cartItems)
        print('----ITEMS inside items----')
        for x in items:
            print(x)
        

    return{'cartItems': cartItems, 'order': order_dict, 'items': items}

    
def guestOrder(request, data):

    print('User is not logged in..')

    print('COOKIES:', request.COOKIES)
    nombre = data['form']['name'].upper()
    apellido = data['form']['last_name'].upper()
    email = data['form']['email']
    dni_cuit = data['dni_cuit']
    telefono = data['form']['phone']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Cliente.objects.get_or_create(
        email=email,
    )
    
    customer.nombre = nombre
    customer.apellido = apellido
    customer.telefono = telefono
    customer.dni_cuit = dni_cuit
    customer.save()

    #order = Compra.objects.create(cliente=customer, completada=False)

    order, created = Compra.objects.get_or_create(cliente=customer, status=None, completada=False)

    for item in items:
        product = Producto.objects.get(id=item['producto']['id'])

        orderItem = OrderItem.objects.create(
            producto=product,
            compra=order,
            quantity=item['quantity']
        )

    return customer, order



def cartData_especial(request):
    
    cart = {'3': {'quantity': 1}}

    print('Cart:', cart)
    items = []
    items_name = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'total_check': 0 ,'shipping': False}
    cartItems = 0

    for item in cart:
        cartItems += cart[item]["quantity"]
        order['get_cart_items'] += cart[item]["quantity"]
    for i in cart:
        try:  
            producto = Producto.objects.get(id=i)
            total = (producto.precio * cart[i]["quantity"])
            order['total_check'] += total
            
            item = {
                'producto': {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'precio': producto.precio,
                    'precio_descuento': producto.precio_descuento,
                    'imageURL': producto.imageURL,
                    'sku':producto.sku
                },
            'quantity': cart[i]['quantity'],
            'get_total': total,
            'get_total_discounted': (producto.precio_descuento * cart[i]["quantity"])
            }

            items.append(item)
            items_name.append(producto.nombre)
            order['get_cart_total'] += total 

        except:
            pass
                 
    return {'cartItems': cartItems, 'order': order, 'items': items}