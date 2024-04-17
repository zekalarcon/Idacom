import os
import django
import xml.etree.cElementTree as ET
import xml.dom.minidom

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "laplanchetta.settings") # project_name nombre del proyecto
django.setup()

from productos.models import Producto

def xml_google():

    productos = Producto.objects.order_by('-precio').all()
   
    if os.path.exists("/var/www/html/productos.xml"):
        os.remove('/var/www/html/productos.xml')

    m_encoding = 'UTF-8'
    x = {
        'xmlns:g':"http://base.google.com/ns/1.0",
        'version':'2.0'
    }

    root = ET.Element('rss', x)
    doc = ET.SubElement(root, "channel")
    ET.SubElement(doc, "title").text = ""
    ET.SubElement(doc, "link").text = ""
    for producto in productos:

        if producto.disponible == True:
            disponible = 'En stock'
        else:
            disponible = 'Sin stock'    

        head = ET.SubElement(doc, "item")
        ET.SubElement(head, "g:id").text = str(producto.sku)
        ET.SubElement(head, "g:title").text = translate(str(producto.nombre)).title()
        ET.SubElement(head, "g:description").text = translate(str(producto.descripcion))
        ET.SubElement(head, "g:link").text = 'https:///%s' % str(producto.slug)
        ET.SubElement(head, "g:image_link").text = 'https:///' + str(producto.imageURL)
        ET.SubElement(head, "g:condition").text = 'Nuevo'
        ET.SubElement(head, "g:availability").text = disponible
        ET.SubElement(head, "g:price").text = str(producto.precio) + ' ' + 'ARS'
        body = ET.SubElement(head, "g:shipping")
        ET.SubElement(body, "g:country").text = 'ARG'
        ET.SubElement(body, "g:service").text = 'Compra superior a $3500 ARS'
        ET.SubElement(body, "g:price").text = '0.00 ARS'
        envio1 = ET.SubElement(head, "g:shipping")
        ET.SubElement(envio1, "g:country").text = 'ARG'
        ET.SubElement(envio1, "g:service").text = 'Compra inferior a $3500 ARS'
        envio2 = ET.SubElement(envio1, "g:price").text = '500.00 ARS'
        ET.SubElement(head, "g:gtin").text = str(producto.e_a_n)
        ET.SubElement(head, "g:brand").text = str(producto.categoria.categoria)
        ET.SubElement(head, "g:mpn").text = str(producto.categoria.categoria).replace(' ','') + str(producto.sku)
        ET.SubElement(head, "g:google_product_category").text = 'Home & Garden > Kitchen & Dining > Kitchen Tools & Utensils'


    dom = xml.dom.minidom.parseString(ET.tostring(root))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    with open("/var/www/html/productos.xml", 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()
          

def translate(text):

    normalMap = {
        'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
        'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
        'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'Ñ': 'N', 'ñ': 'n',
        'Ç': 'C', 'ç': 'c',
        '§': 'S',  '³': '3', '²': '2', '¹': '1',
        '®': ''
    }

    normalize = str.maketrans(normalMap)
    text_normalized = text.translate(normalize)

    return text_normalized 


xml_google()