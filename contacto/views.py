from django.shortcuts import render, redirect
from .forms import ContactoForm
from decouple import config
from django.core.mail import send_mail
from django.http import JsonResponse
import json, requests
from utils.utils import cartData
from pyisemail import is_email



def contacto_view(request):

    contacto_form = ContactoForm(request.POST or None)

    if request.method == "GET":

        data = cartData(request)
        cartItems = data['cartItems']

        context = {
            'contacto_form': contacto_form,
            'cartItems': cartItems,
            'recaptcha_site_key': config('SECRET_SITE_KEY')
        }

        return render(request, "contacto/contacto.html", context)

    else:

        return redirect('contacto')    

            
def mandar_mensaje(request):

    data_json = json.loads(request.body)
    titulo = 'Consulta idacom.com.ar'
    mensaje = data_json['mensaje'] + '\n\n' + data_json['email']
    email_from = config('EMAIL_HOST_USER')
    to_email = [config('EMAIL_HOST_USER'),]
   
    #detailed_result_with_dns = is_email(data_json['email'], check_dns=True, diagnose=True)
    bool_result_with_dns = is_email(data_json['email'], check_dns=True)

    #print('RESULTADO:', bool_result_with_dns)

    # captcha verification
    data = {
        'response': data_json['captcha'],
        'secret': config('SECRET_KEY_CAPTCHA')
    }

    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()

    if result_json['success'] == True and bool_result_with_dns == True:

        try:
           
            send_mail(titulo, mensaje, email_from, to_email)

            data = [{
                'mensaje':'enviado'
            }]

        except:

            data = [{
                'mensaje':'error'
            }]

    else:

        if bool_result_with_dns == False and result_json['success'] == True:

            data = [{
                'mensaje':'email invalido'
            }]

        else:

            data = [{
                    'mensaje':'robot'
                }]

    return JsonResponse(data, safe=False)



def nosotros_view(request):

    data = cartData(request)
    cartItems = data['cartItems']
 
    context = {
        'cartItems': cartItems,
    }

    return render(request, "nosotros/nosotros.html", context)
