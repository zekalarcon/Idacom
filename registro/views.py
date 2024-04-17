from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from decouple import config
from django.contrib.auth.models import User
from cliente.models import Cliente
from django.contrib.auth.hashers import make_password
from utils.views import captcha_validador


def register_view(request):
       
    context = {
        'recaptcha_site_key': config('SECRET_SITE_KEY')
    }
    return render(request, "register/register.html", context)


def login_view(request):
    
    context = {
        'recaptcha_site_key': config('SECRET_SITE_KEY')
    }

    return render(request, 'registration/login.html', context)    


def logout_view(request):
    logout(request)
    return redirect('inicio')   


def registrar_cliente(request):

    data_json = json.loads(request.body)
    usuario = data_json['email']
    nombre = data_json['nombre'].upper()
    apellido = data_json['apellido'].upper()
    telefono = data_json['telefono']
    password1 = data_json['password1']

    try:
        user = User.objects.create(username=usuario, first_name=nombre, last_name=apellido, email=usuario, password=make_password(password1))
        # Creating the customer object
        Cliente.objects.create(user= user, nombre=nombre, apellido=apellido, telefono=telefono, email=usuario)

        data = [{
                'mensaje':'guardado'
            }]
        
    except:

        data = [{
                'mensaje':'error'
            }]

    return JsonResponse(data, safe=False)       


def loguearse(request):

    data_json = json.loads(request.body)
    usuario = data_json['usuario']
    password = data_json['password']
    captcha = data_json['captcha']

    result_captcha = captcha_validador(captcha)

    print('usuario:', usuario)
    print('recaptcha:', result_captcha)

    if result_captcha['success'] == True:

        user = authenticate(request, username=usuario, password=password)

        if user is not None and user.is_active == True:

            login(request, user)

            data = [{
                    'mensaje':'logueado'
                }]

        else:

            data = [{
                    'mensaje':'error'
                }]

        return JsonResponse(data, safe=False)

    else:

        data = [{
                    'mensaje':'robot'
                }]

        return JsonResponse(data, safe=False)