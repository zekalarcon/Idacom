from django import forms
from correos.models import Correo
from cliente.models import Cliente
from envio.models import DatosEnvio

#class CorreoForm(forms.Form):
#    correos = forms.ChoiceField(choices=[(correo.nombre,(f'{correo.nombre} $ {str(correo.precio)}')) for correo in Correo.objects.all()], widget=forms.RadioSelect(attrs={'class': 'browser-default'}))
    
#    class Meta:
#        model = Correo
#        fields = ['correos']


        
class UsuarioForm(forms.Form):

    nombre = forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'type':'search', 'autocomplete': 'off', 'placeholder': 'Nombre', 'pattern':'^[A-Za-z\s]+$', 'title':'Solo letras'}))
    apellido = forms.CharField(max_length=30, min_length=3, required=True, widget=forms.TextInput(attrs={'type':'search', 'autocomplete': 'off', 'placeholder': 'Apellido', 'pattern':'^[A-Za-z\s]+$', 'title':'Solo letras'}))
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'autocomplete': 'off' , 'placeholder': 'Correo electronico'}))
    telefono = forms.IntegerField(min_value=111111111, max_value=99999999999999, required=True, widget=forms.TextInput(attrs={'type':'search', 'autocomplete': 'off', 'placeholder': 'Telefono', 'pattern':'^(1|2|3)([0-9])+$', 'title':'C.Area sin 0 + Tel. sin 15'})) 
    dni_cuit = forms.IntegerField(min_value=00000000, max_value=99999999999, required=True, widget=forms.TextInput(attrs={'type':'search', 'autocomplete': 'off', 'placeholder': 'Dni o Cuit', 'pattern':'^[0-9]+$', 'title':'Solo numeros'})) 
    
    class Meta:
        model  = Cliente
        fields = [
            'nombre',
            'apellido',
            'email',
            'telefono',
            'dni_cuit'
        ]


class EnvioForm(forms.Form):

    indicaciones = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'name':'Indicaciones', 'autocomplete':'off', 'placeholder': 'Indicaciones cartero', 'type':'text'}))
    
    class Meta:
        model  = DatosEnvio
        fields = [
            'indicaciones'
        ]


class DecidirTarjetaForm(forms.Form):
    quotas = (
        (None,'Cuotas'),
        ('1','1 CFT: 0,00%'),
        ('3','3 CFT: 0,00%'),
        ('6','6 CFT: 0,00%'),
        ('12','12 CFT: 18,18%'),
        ('18', '18 CFT: 28,84%'),
        ('24', '24 CFT: 35,83%')
    )
    number = forms.IntegerField( label='Numero tarjeta', required=True, widget=forms.TextInput(attrs={'maxlength':'22','pattern':'^[0-9 ]+$', 'placeholder':'Numero tarjeta', 'title':'Solo numeros, entre 13 y 19 digitos.'}))
    cvc = forms.IntegerField(label='CVV', required=True, widget=forms.TextInput(attrs={'maxlength':'4','pattern':'^[0-9]+$', 'placeholder':'CVV', 'title':'Solo 3 o 4 numeros.'}))
    expiry = forms.IntegerField( label='Vcto', required=True, widget=forms.TextInput(attrs={'maxlength':'7', 'placeholder':'Vcto','title':'Solo numeros y /'}))
    name = forms.CharField(label='Nombre titular', required=True, widget=forms.TextInput(attrs={'pattern':'^[A-Za-z\s]+$', 'placeholder':'Nombre titular', 'title':'Nombre completo, tal cual aparece en la tarjeta.'}))
    cuotas = forms.ChoiceField(choices=quotas, label='Cuotas', required=True, widget=forms.Select(attrs={'class': 'browser-default', 'placeholder':'Cuotas'}))
    numero_documento = forms.CharField(max_length=18, label='Numero DNI', required=True, widget=forms.TextInput(attrs={'type':'search', 'autocomplete': 'off', 'pattern':'^[a-zA-Z0-9.-]*$', 'placeholder':'Numero DNI', 'title':'Numeros, letras y -'}))
