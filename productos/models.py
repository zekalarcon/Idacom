from django.db import models
import barcode
from barcode.writer import ImageWriter
import io, os
from django.core.files import File
from django.utils import timezone
from django.utils.text import slugify
from cliente.models import Cliente
from random import randint
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import FileExtensionValidator

def file_size(value): 
    limit = 1 * 1024 * 1024
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png','.webp','.jpg']
  
    if not ext in valid_extensions:
        raise ValidationError('La imagen solamente puede ser : .png, .jpg, o .webp')
    if value.size > limit:
        raise ValidationError('La imagen no debe exceder 1 Mb. de peso!')
    if value.height != value.width:
        raise ValidationError("La imagen debe ser cuadrada. Ej. 500x500")


def type_img(value):
    ext = os.path.splitext(value.name)
    valid_extensions = ['.png','.webp','.jpg']
    
    if not ext.lower() in valid_extensions:
        raise ValidationError('La imagen solamente puede ser : .png, .jpg, o .webp') 

class Categoria(models.Model):

    categoria = models.CharField(max_length=200, null=True, unique=True)

    def clean(self):
        self.categoria  = self.categoria.upper()

    def __str__(self):
        return str(self.categoria)  


class Producto(models.Model):

    nombre = models.CharField(max_length=200, unique=True, null=False)
    nombre_abreviado = models.CharField(max_length=100, null=False, default='')
    slug = models.SlugField(max_length=200, default='', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, default=None, on_delete=models.SET_NULL, null=True)
    calificacion = models.DecimalField(max_digits=10, decimal_places=1, default=4.1)
    disponible = models.BooleanField(default=None)
    combo = models.BooleanField(default=None)
    especial = models.BooleanField(default=False, null=True, blank=True)
    precio = models.DecimalField(max_digits=100, decimal_places=2)
    precio_tachado = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    precio_descuento = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    sku = models.CharField(max_length=5, unique=True, null=False, default='')
    e_a_n = models.CharField(max_length=20, null=False, blank=True, default='0')
    bar_code = models.ImageField(upload_to = 'images/barcode', blank=True, null=True)
    imagen_portada = models.ImageField(upload_to = 'images/portada', null=True, blank=True, validators=[file_size])
    descripcion = models.TextField(max_length=1500, null=True, default='Descripcion')
    caracteristicas = models.TextField(max_length=1500, null=True, default='Caracteristicas')
    fecha_added = models.DateTimeField(default=timezone.now)
  
    def clean(self):
        self.nombre            = self.nombre.upper()
        self.nombre_abreviado  = self.nombre_abreviado.upper()
        self.sku               = self.sku.upper()

    def save(self, *args, **kwargs):
        bar_ean = barcode.get_barcode_class('code39')
        ean = bar_ean(f'{self.sku}0000000', writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer)
        self.bar_code.save(f'{self.nombre}-barcode.png', File(buffer), save=False)
        self.slug = slugify(self.nombre)

        return super().save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.imagen_portada.url 
        except:
            url = ''
        return url 

    @property
    def barcodeURL(self):
        try:
            url = self.bar_code.url 
        except:
            url = ''
        return url 

    @property
    def get_10_off(self):
        product_price = float(self.precio)-((float(self.precio) * 10) / 100)
        print("PRODUCTO DESCUENTO", product_price)
        return product_price
    
    @property
    def get_15_off(self):
        product_price = float(self.precio)-((float(self.precio) * 15) / 100)
        print("PRODUCTO DESCUENTO", product_price)
        return product_price

    @property
    def get_10_off_dis(self):
        product_price = float(self.precio_descuento)-((float(self.precio_descuento) * 10) / 100)  
        return product_price

    @property
    def get_15_off_dis(self):
        product_price = float(self.precio_descuento)-((float(self.precio_descuento) * 15) / 100)
        return product_price

    @property
    def get_calificacion(self):

        if self.calificacion == 0.0:
            score = 4.1
        else:
            score = self.calificacion
        return str(score)

    @property
    def get_cantidad_calificaciones(self):
        calificaciones = self.productoscalificacion_set.all()

        if calificaciones.count() == 0:
            cantidad_calificaciones = randint(2,10)
        else:
            cantidad_calificaciones = calificaciones.count()

        return str(cantidad_calificaciones)

    @property
    def update_calificacion(self, *args, **kwargs):
        calificaciones = self.productoscalificacion_set.all()
        puntuacion = sum([item.calificacion for item in calificaciones])

        self.calificacion = puntuacion / int(calificaciones.count())

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)    
    

class ImagenesProducto(models.Model):
    
    post = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE)
    imagenes = models.FileField(upload_to = 'images/details')

    def clean(self):

        width, height = get_image_dimensions(self.imagenes)
        ext = os.path.splitext(self.imagenes.name)[1]

        valid_extensions = ['.png','.webp','.jpg']
        print('ext:', ext)
        
        if not ext in valid_extensions:
            raise ValidationError('La imagen solamente puede ser : .png, .jpg, o .webp')
        if width != height:
            raise ValidationError("La imagen debe ser cuadrada. Ej. 500x500")
        if self.imagenes.size > 1048576:
            raise ValidationError('La imagen no debe exceder 1 Mb. de peso!')

    
    def __str__(self):
        return str(self.post)  


class ItemsCombo(models.Model):
    
    productos = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE, related_name='productoss')
    item = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE, related_name= 'items' )
    cantidad = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_items_combo(self):

        product = {'items':{
                'nombre':self.item,
                'cantidad':self.cantidad,
                
            }
        }

        return product

    def __str__(self):
        return str(self.productos)
  

class ProductosCalificacion(models.Model):
    
    compra_id = models.IntegerField(null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    calificacion = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    comentario = models.TextField(max_length=400, null=True, blank=True, default='')
    fecha = models.DateTimeField(default=timezone.now)
  
    def __str__(self):
        return str(self.calificacion)