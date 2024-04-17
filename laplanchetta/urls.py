"""laplanchetta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from cliente.views import panel_cliente_view, calificar_producto, eliminar_cuenta
from productos.views import productos_view, detail_view
from contacto.views import contacto_view, mandar_mensaje, nosotros_view
from compra.views import carrito_view
from envio.views import create_preference, decidir, email_verification, address_finder ,notifications, checkout_view
from registro.views import register_view, login_view, logout_view, registrar_cliente, loguearse
from updateItem.views import updateItem
from processOrder.views import processOrder
from home.views import home_view
from ofertas_especiales.views import ofertas_especiales_view
from utils.views import statistics_view, etiquetas_view, email_validador, update_slider
from django.views.static import serve 
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductosSitemap, StaticSitemap
from deploy.views import AutoDeploy

sitemaps = {
    'static':StaticSitemap,
    'productos':ProductosSitemap,
}

urlpatterns = [
 
    path('crm/', admin.site.urls),
    path('graficos/', include('utils.urls')),
    path('statistics/', statistics_view, name='shop-statistics'),
    path('etiquetas/', etiquetas_view, name='etiquetas'),
    path('email_validador/', email_validador, name='email_validador'),
    path('update_slider/', update_slider, name='update_slider'),
    path('deploy/', AutoDeploy, name='deploy'),
    path('', home_view, name='inicio'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('panelcliente/', panel_cliente_view, name='panelcliente'),
    path('eliminar_cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('calificar_producto/', calificar_producto, name='calificar_producto'),
    path('productos/', productos_view, name='productos'),
    path('nosotros/', nosotros_view, name='nosotros'),
    path('contacto/', contacto_view, name='contacto'),
    path('mandar_mensaje/', mandar_mensaje, name='mandar_mensaje'),
    path('carrito/', carrito_view, name='carrito'),
    path('checkout/', checkout_view, name='checkout'),
    path('email_verification/', email_verification, name='email_verification'),
    path('address_finder/', address_finder, name='address_finder'),
    path('notifications/', notifications, name='notifications'),
    path('decidir/', decidir, name='decidir'),
    path('create_preference/', create_preference, name='create_preference'),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    path('registro/', register_view, name='registro'),
    path('registrar_cliente/', registrar_cliente, name='registrar_cliente'),
    path('loguearse/', loguearse, name='loguearse'),
    path('acceso/', login_view, name='login'),
    path('salir/', logout_view, name='logout'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), 
        name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
        name='password_reset_complete'),
    path('ofertas_especiales/', ofertas_especiales_view, name="ofertas_especiales"),
    path('<slug:slug>/', detail_view, name='detail'),
    #re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    #re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#admin.site.site_header = ''          # default: "Django Administration"
#admin.site.index_title = 'Features area'                 # default: "Site administration"
#admin.site.site_title = 'IDACOM sitio administrativo' # default: "Django site admin"