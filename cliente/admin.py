from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'nombre', 'apellido', 'email']
    ordering = ['user']

admin.site.register(Cliente, ClienteAdmin)