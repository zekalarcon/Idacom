from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    username = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electronico', 'autocomplete': 'none', 'type': 'email'}))
    first_name = forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'autocomplete': 'off', 'type': 'search'}))
    last_name =  forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido', 'autocomplete': 'off', 'type': 'search'}))
    phone = forms.IntegerField(min_value=111111111, max_value=99999999999999, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'pattern':'^[0-9]+$', 'title':'Solo numeros', 'autocomplete': 'off', 'type': 'number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar contraseña'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    
