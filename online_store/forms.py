from django import forms
from phonenumber_field.formfields import PhoneNumberField
    
class Panier_form(forms.Form):
    number= PhoneNumberField(region='ML',label='Numéro')
    adresse= forms.CharField(max_length=30,label="Résidence")