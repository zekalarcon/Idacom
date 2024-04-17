from django.db import models
from django.utils import timezone
from cliente.models import Cliente
from productos.models import Producto, ProductosCalificacion

class Compra(models.Model):
    STATUS = (
            ('PENDIENTE', 'PENDIENTE'),
            ('PREPARANDO ORDEN', 'PREPARANDO ORDEN'),
            ('LISTA PARA RETIRAR', 'LISTA PARA RETIRAR'),
            ('EN CAMINO', 'EN CAMINO'),
            ('ENTREGADO', 'ENTREGADO'),
            )

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)        
    completada = models.BooleanField(default=False, null=True, blank=False)
    medio_de_pago = models.CharField(max_length=100, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    fecha_compra = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    correo = models.CharField(max_length=100, null=True)
    calificacion = models.ForeignKey(ProductosCalificacion, on_delete=models.SET_NULL, blank=True, null=True) 

    def clean(self):
        try:
            self.medio_de_pago = self.medio_de_pago.upper()
            self.correo        = self.correo.upper()
        except:
            pass

    def __str__(self):
        return str(self.transaction_id)
  
    
    def total_sin_descuento(orderitems, items_sku, items_quantity):
           
        if 'CB016' in items_sku and items_quantity > 1:
            total = sum([item.get_total if item.get_total_discounted == 0 and item.producto.especial == False else item.get_total_discounted if item.get_total_discounted != 0 and item.producto.especial == False else 0 for item in orderitems])
            
        elif 'CB016' in items_sku and items_quantity == 1:
            total = sum([item.get_total for item in orderitems])
            
        elif 'CB001' in items_sku and items_quantity > 1:
            total = sum([item.get_total if item.get_total_discounted == 0 and item.producto.especial == False else item.get_total_discounted if item.get_total_discounted != 0 and item.producto.especial == False else 0 for item in orderitems])
            
        elif 'CB001' in items_sku and items_quantity == 1:
            total = sum([item.get_total for item in orderitems])

        else:
            total = sum([item.get_total if item.producto.especial == False else 0 for item in orderitems])
        
        return total

    def total_especial(orderitems):
        t = 0
        for x in orderitems:
            if x.producto.especial == True:
                t += x.producto.precio * x.quantity
        return t        

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        items_sku = [item.producto.sku for item in orderitems]
        items_quantity = sum([item.quantity for item in orderitems])
        
        print('----get_cart_total @property----')
        print('NOMBRES ITEMS:', items_sku)

        especial_total = Compra.total_especial(orderitems)
        total = Compra.total_sin_descuento(orderitems, items_sku, items_quantity)
        print('TOTAL model compra :', total)

        if float(total) >= 9000 or float(especial_total) >= 9000:
            porcentaje = (int(10)*float(total)) / 100
            t = float(total) - porcentaje
            total = t + float(especial_total)
            print('TOTAL MAYOR A 9K O ESPECIAL TOTAL MAYOR 9K:', total )

        #elif float(total) >= 10000:
            #porcentaje = (int(15)*float(total)) / 100
            #total = float(total) - porcentaje
            #print('TOTAL 15% OFF:', total )
            
        else:
            total = float(total) + float(especial_total)

        return total

    @property
    def total_check(self):
        orderitems = self.orderitem_set.all()
        items_name = [item.producto.nombre for item in orderitems]
        items_quantity = sum([item.quantity for item in orderitems])
        total = Compra.total_sin_descuento(orderitems, items_name, items_quantity)  
        return total

    @property
    def total_check_especial(self):
        orderitems = self.orderitem_set.all()
        total = Compra.total_especial(orderitems)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_products(self):
        orderitems = self.orderitem_set.all()
        products = [item.get_products for item in orderitems]
        return products


class OrderItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)        
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True)        
    quantity = models.IntegerField(default=0, null=True, blank=True)
    fecha_added = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Item Comprado"
        verbose_name_plural = "Items Comprados"
    
    def __str__(self):
        return '%s' % (self.compra)
        
    @property
    def get_total(self):
        total = self.producto.precio * self.quantity
        return total     

    @property
    def get_total_discounted(self):
        total_discounted = self.producto.precio_descuento * self.quantity
        return total_discounted

    @property
    def get_products(self):
        product = {'producto':{
            'id':self.producto.id,
            'nombre':self.producto.nombre,
            'nombre_abreviado':self.producto.nombre_abreviado,
            'imageURL':self.producto.imageURL,
            'precio':self.producto.precio,
            'precio_descuento':self.producto.precio_descuento,
            'precio_tachado':self.producto.precio_tachado,
            'sku':self.producto.sku,
            'slug':self.producto.slug,
            'especial':self.producto.especial
        },
        'quantity':self.quantity,
        'get_total':self.get_total,
        'get_total_discounted':self.get_total_discounted
        }

        return product

