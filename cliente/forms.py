from django import forms
from .models import Cliente


class PanelClienteForm(forms.Form):

    nombre = forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre..', 'pattern':'^[A-Za-z\s]+$', 'title':'Solo letras'}))
    apellido = forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido..', 'pattern':'^[A-Za-z\s]+$', 'title':'Solo letras'}))
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electronico..'}))
    telefono = forms.IntegerField(min_value=111111111, max_value=99999999999999, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono..', 'pattern':'^[0-9]+$', 'title':'Solo numeros'}))   
        
    class Meta:
        model  = Cliente
        fields = [
            'nombre',
            'apellido',
            'email',
            'telefono'
       
        ]

