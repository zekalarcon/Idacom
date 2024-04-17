from django.db import models
from django.utils import timezone
from cliente.models import Cliente
from compra.models import Compra


class DatosEnvio(models.Model):
    fecha_added = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)        
    compra = models.ForeignKey(Compra, on_delete=models.SET_NULL, null=True) 
    correo = models.CharField(max_length=100, null=True)
    numero_de_seguimiento = models.CharField(max_length=200, null=True)
    numero_de_retiro = models.CharField(max_length=200, null=True)
    etiqueta_impresa = models.BooleanField(default=False, null=True, blank=False)       
    direccion = models.CharField(max_length=200, null=False)
    ciudad = models.CharField(max_length=200, null=False)
    provincia = models.CharField(max_length=200, null=False)
    codigo_postal = models.CharField(max_length=200, null=False)
    telefono = models.CharField(max_length=200, null=True)
    indicaciones = models.CharField(max_length=500, null=True, blank=True)

    def clean(self):
        try:
            self.direccion    = self.direccion.upper()
            self.ciudad       = self.ciudad.upper()
            self.provincia    = self.provincia.upper()
            self.correo       = self.correo.upper()
            self.indicaciones = self.indicaciones.upper()
            self.numero_de_seguimiento = self.numero_de_seguimiento.upper()
            self.numero_de_retiro = self.numero_de_retiro.upper()
        except:
            pass

    def __str__(self):
        return str(self.cliente)


class Provincias(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    codigo31662 = models.CharField(max_length=10, null=True)

    def clean(self):
        self.nombre = self.nombre.title()
        

class Localidad(models.Model):
    provincia_id = models.ForeignKey(Provincias, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=50, null=True)
    codigo_postal = models.IntegerField(null=True)

    def clean(self):
        self.nombre = self.nombre.upper()
