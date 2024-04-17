from django.db import models

# Create your models here.


class Correo(models.Model):

    nombre = models.CharField(max_length=200, null=True, unique=True)
    precio = models.DecimalField(max_digits=100, decimal_places=2)
    imagen = models.ImageField(upload_to = 'images/correos', null=True, blank=True)
    
    def clean(self):
        self.nombre  = self.nombre.upper()
    

    @property
    def imageURL(self):
        try:
            url = self.imagen.url 
        except:
            url = ''
        return url 


    def __str__(self):
        return str(self.nombre) 