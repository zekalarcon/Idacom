from django import template
from productos.models import Producto

register = template.Library()

@register.simple_tag()
def percentage(porcentje, total):
	t= (float(total) - float((int(porcentje)*float(total)) / 100))
	return f'{t:.0f}'


@register.simple_tag()
def promos_navbar(promo, total):
	t = float(promo) - float(total)
	return f'{t:.0f}'


