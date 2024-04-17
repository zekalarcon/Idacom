from django import forms

class ContactoForm(forms.Form):
    email_contacto = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'class': 'form-control','autocomplete': 'off' , 'placeholder': 'Correo electronico'}))
    mensaje = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control','col':10,"rows":3,'style': 'font-size: medium', 'placeholder': 'Mensaje'}))