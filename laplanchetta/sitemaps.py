from django.contrib.sitemaps import Sitemap
from productos.models import Producto
from django.urls import reverse
 
 
class ProductosSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Producto.objects.all()

    def lastmod(self, obj):
        return obj.fecha_added
        
    def location(self,obj):
        return '/%s' % (obj.slug)


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return ['inicio', 'productos', 'nosotros', 'contacto', 'login']

    def location(self, item):
        return reverse(item)