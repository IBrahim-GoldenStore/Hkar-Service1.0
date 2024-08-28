from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

#  NOUS UTILISONS LE PROTOTYPE ICI

class Userform(UserCreationForm):
    email= forms.EmailField(required=True, label='E_mail')

    class META:
        model= User
        fields= ('username','email','password1','password2')

    def save(self, commit= True):
        user= super().save(commit= False) # "commit= False" cree un instance sans l'enrigistrez dans la base de donnees
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class Connectform(AuthenticationForm):
    email= forms.EmailField(required= True, label='E_mail',)

class Message(forms.Form):
    message= forms.CharField(widget= forms.Textarea(attrs={'class': "conctact_form"}),label="Avis")
