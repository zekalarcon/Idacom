from django.contrib import admin
from .models import Producto, ImagenesProducto, ItemsCombo, Categoria, ProductosCalificacion

admin.site.register(Categoria)
 
class ImagenesProductoAdmin(admin.TabularInline):
    model = ImagenesProducto

class ItemsComboAdmin(admin.TabularInline):
    model = ItemsCombo
    fk_name = "productos"  

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Producto.objects.filter(combo=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

 
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenesProductoAdmin, ItemsComboAdmin]
    list_display = ['nombre', 'sku', 'precio', 'categoria', 'disponible', 'calificacion', 'combo', 'especial']
    list_filter = ('categoria', 'disponible', 'combo', 'especial')
    search_fields = ('nombre', 'sku', 'calificacion', 'precio' )
    ordering = ['precio']
    exclude = ('precio_descuento',)

    class Meta:
       model = Producto


#@admin.register(ProductosCalificacion)
#class ProductosCalificacionAdmin(admin.ModelAdmin):
#    list_display = ['producto', 'calificacion', 'cliente']
#    ordering = ['producto']
#    exclude = ('comentario',)

#    class Meta:
#       model = ProductosCalificacion