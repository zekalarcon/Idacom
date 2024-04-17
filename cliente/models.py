from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    user     = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE )
    nombre   = models.CharField(max_length=40, null=False)
    apellido = models.CharField(max_length=40, null=False)
    email    = models.EmailField(unique=True, max_length=200, null=False)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    dni_cuit = models.CharField(max_length=40, null=False, blank=True)

    def clean(self):
        self.nombre   = self.nombre.upper()
        self.apellido = self.apellido.upper()
        
    
    def __str__(self):
        return '%s' % (self.user)