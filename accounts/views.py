from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout,login  # importation des fonction de connexion,deconnexion et verification
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
# nouvelles imporation et changement
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.forms import AuthenticationForm
from django.utils.html import strip_tags
from online_store.models import Jeton



# Create your views here.
def receivers():
    receiver= User.objects.filter(is_staff=True)
    emails= receiver.values_list('email',flat=True)
    return emails


def connexion(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(username= username,password= password)
        if user is not None:
            login(request, user)
            next_url= request.GET.get('next')
            return redirect(next_url or 'store:index')
        else:
            messages.info(request, "Données incorrect")
    form= AuthenticationForm()

    return render(request,'account/connexion.html', {'form': form})


def deconnexion(request):
    user= logout(request)
    return redirect('store:index')

def success(request):
       return render(request,'account/success.html',{})

from django.contrib.auth.models import User
def compte(request):
    if request.method == 'POST':
        form= Userform(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            form.save()
            context={
                'username': username,
                'contact':'hkarservice.team@gmail.com'
            }
            subject="Inscription sur Hkar-Service"
            email_content= render_to_string('account/inscription.html',context)
            email_brute= strip_tags(email_content)

            msg= EmailMultiAlternatives(subject,email_brute,'',[email])
            msg.attach_alternative(email_content,"text/html")
            msg.send()

            #send_mail(subject,email_content,'',[email],html_message=email_content)
            user= authenticate(username= username,passwords= password, email= email)
            login(request,user)
            #Jeton.objects.create(user=user)
            return redirect('account:success')
    else:
        form = Userform()

    return render(request, 'account/account.html',{'form': form,})
@login_required
def contacts(request):
    message= Messages_site.objects.all()
    avis=set()
    for i in range(0,11):
        if i < len(message):
            avis.add(message[i])
    if request.method == "POST":
        form_c = Message(request.POST)
        if form_c.is_valid():
            user= request.user
            name= user.username
            e_mail= user.email
            contenu= form_c.cleaned_data['message']
            message_base= Messages_site.objects.create(nom= name.capitalize(), e_mails= e_mail, message= contenu)
            message_base.save()
            return redirect('account:cont')
    else:
        form_c= Message()

    return render(request, 'account/nos_contact.html',{"form": form_c,'avis':avis})

def send_reset_email(request):
    if request.method == "POST":
        form= PasswordForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data['email']
            try:
                user= User.objects.get(email=email)
            except:
                return render(request, 'account/error.html',{})
            if user:
                sujet= "Réinitialisation de votre mot de passe"
                context={
                    'username': user.username,
                    'domain': get_current_site(request).domain,
                    'uid64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https'#utilser https en production
                }
                email_content= render_to_string('account/email.html',context)
                email_brute= strip_tags(email_content)

                msg= EmailMultiAlternatives(sujet,email_brute,'',[email])
                msg.attach_alternative(email_content,"text/html")
                msg.send()

                # send_mail(sujet,email_brute,'',[user.email],html_message=email_content)
                send_mail(sujet, "Demande de modification de mots de passe par: {} \n Email:{}".format(user.username,user.email),'goldensotrebox@gmail.com',receivers())
                return render(request,'account/sucess_send.html',{'value': 'Email envoyer avec succès !'})
        else:
            return render(request, 'account/error.html',{})
    else:
        form= PasswordForm()

    return render(request, 'account/reset.html', {'form': form})

def set_new_password(request, uid, token):
    user_id= force_str(urlsafe_base64_decode(uid))
    user= User.objects.get(pk=user_id)
    if user is not None and default_token_generator.check_token(user,token):
        if request.method == 'POST':
            form= SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'account/sucess_send.html',{'value': "Mots de passe Réinitialiser avec succès"})
        else:
            form= SetPasswordForm(user)

    return render(request,'account/setpassword.html',{'form': form})

from online_store.models import Commande,Panier,Statue
@login_required
def profil_view(request):

    user=request.user
    do= Statue.objects.get(statue__icontains='Effectuer')
    wait= Statue.objects.get(statue__icontains='attente')
    commande_en_cours= Commande.objects.filter(user=user,statue=wait)
    commande_effectuer= Commande.objects.filter(user=user,statue=do).count()
    panier= Panier.objects.filter(user=user)
    montant_panier=0
    montant_commande=0

    for i in panier:
        montant_panier += i.quantity * i.price

    for i in commande_en_cours:
        montant_commande += i.quantity * i.montant

    first_letter= user.username[0].capitalize()

    context={
        'first_letter':first_letter,
        'commandes_effectuer':commande_effectuer,
        'commande_en_cours': commande_en_cours,
        'paniers':panier,
        'montant_panier': montant_panier,
        'montant_commande': montant_commande
    }
    return render(request,'account/profil.html',context)
