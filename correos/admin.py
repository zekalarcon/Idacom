from django.contrib import admin
from .models import Correo


class CorreoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']
    ordering = ['precio']

admin.site.register(Correo, CorreoAdmin)