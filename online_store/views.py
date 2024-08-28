from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def fiche(produits):
    category_list= set() # set() cree un ensemble sans doublon
    for produit in produits:
        if produit.category.name:
            target_category= Category.objects.get(name= produit.category.name)
            category_list.add(target_category)
    return category_list

def receivers():
    receiver= User.objects.filter(is_staff=True)
    emails= receiver.values_list('email',flat=True)
    return emails
# Create your views here.
 
 # recuperation des differents produits 
def index(request):
    category= Category.objects.all()
    produit_list= Products.objects.all()
    search= request.GET.get('contain') # recuperation de la valeur via son nom dans le formulaire
    if search !="" and search is not None:# verification
        produit_list= Products.objects.filter(name__icontains=search.strip())  # flitrez les donnees selon la valeur rentrez notez que <__icontains> s'utilise sur le champs qui doit etre verifie sans intermediaire du point

    context= {
        'category': category,
        'category_list': fiche(produit_list),
        'produit_list': produit_list,
        'liens': Lien.objects.all()
    }

    return render(request, 'onlineStore/index.html',context)
    

def produit(request):
    produit_list= Products.objects.all()
    
    search= request.GET.get('contain') # recuperation de la valeur via son nom dans le formulaire
    if search !="" and search is not None: # verification
        produit_list= Products.objects.filter(name__icontains=search.strip())  # flitrez les donnees selon la valeur rentrez notez que <__icontains> s'utilise sur le champs qui doit etre verifie sans intermediaire du point
    paginator= Paginator(produit_list,16) # recuperation et repartitions des produits par page selon le nombre indiquer
    page= request.GET.get('page') # recuperations du page correspondants
    produit_list= paginator.get_page(page)  # assignations a la liste ancienne des produits qui correspondent a la page
    
    context={
        'category_list': fiche(produit_list),
        'produit_list': produit_list,
        'liens': Lien.objects.all()
    }

    return render(request,'onlineStore/produits.html',context)

def trend(request, category_name):
    category= Category.objects.get(name=category_name)
    category_list=set()
    category_list.add(category)
    produit_list= Products.objects.filter(category= category.id)

    return render(request, 'onlineStore/produits.html',{'produit_list': produit_list,'category_list':category_list})

# recuperation d'un article 
def article(request,id_prod):
    article= get_object_or_404(Products, slug= id_prod)
    if request.method == "POST":
        form = Panier_form(request.POST)
        user = request.user   # recupere l'utilsteur actuellement connectez
        if form.is_valid():
            # recupreration des donnees depuis un formulaire
            name = user.username
            number= form.cleaned_data['number']
            adress= form.cleaned_data['adresse']
            email= user.email

            # envois d emai
            sujet= 'Nouvelle commande de la part de {}'.format(name)
            contenu=  "Numero telephonique: {} ,\n E_mail: {},\n Produit &  Quantite: {},\n Montant du Commande: {},\n Localisation: {},\n Achat directe".format(number,email,article.name,article.price,adress,)
            send_mail(sujet,contenu,'goldensotrebox@gmail.com',receivers())


            panier_registration= Commande.objects.create(user= user,number= number, adresse= adress,name_and_quantity= article.name,montant= article.price)
            return render(request, 'onlineStore/success.html',{})
        else:
            return render(request, 'onlineStore/error.html')
    else:
        form= Panier_form()

    return render(request, "onlineStore/article.html",{"article": article,'form':form})

# traitement du panier
@login_required
def panier(request):
    panier =  Panier.objects.filter(user= request.user)
    if panier is not None:
        commande_list= []
        montant=[]                    # Creation d'une table vide qui vas contenir tout le montant de chaque produit
        for item in panier:           # parcourir la liste d'objets "panier" tout en associant chaque objet a item
            montant.append(item.quantity*item.price)    #Grace a la methode append() nous recuperons le montant(quantite x prix) de chaque item et l'ajoutez au table montant 
            commande_list.append((item.name,item.quantity))
        if request.method == "POST":
            form = Panier_form(request.POST)
            user = request.user   # recupere l'utilsteur actuellement connectez
            if form.is_valid():
                # recupreration des donnees depuis un formulaire
                name = user.username
                number= form.cleaned_data['number']
                # if len(str(number)) != 8:
                #     return redirect('store:panier')
                adress= form.cleaned_data['adresse']
                email= user.email
                # envois d emai
                sujet= 'Nouvelle commande de la part de {}'.format(name)
                contenu=  "Numero telephonique: {} ,\n E_mail: {},\n Produit &  Quantite: {},\n Montant du Commande: {},\n Localisation: {},\n Via le panier".format(number,email,commande_list,sum(montant),adress,)
                send_mail(sujet,contenu,'goldensotrebox@gmail.com',receivers())


                panier.delete()
                panier_registration= Commande.objects.create(user= user,number= number, adresse= adress,name_and_quantity= commande_list,montant= sum(montant))
                return render(request, 'onlineStore/success.html',{})
            else:
                return render(request, 'onlineStore/error.html')
        else:
            form= Panier_form()

        return render(request, 'onlineStore/panier.html', {'panier': panier,'montant':sum(montant),'form': form})     # Nous retournons la table montant tout en faisant la somme de ces elements ( sum() )
    else:
        return render(request, 'onlineStore/panier.html', {'panier': '','montant':sum(montant),'form': form})     # Nous retournons la table montant tout en faisant la somme de ces elements ( sum() )


@login_required
def ajouter(request, article_id):
    produit= Products.objects.get(pk= article_id)
    panier, created= Panier.objects.get_or_create(name= produit.name,price= produit.price,user= request.user)
    if not created:
        panier.quantity += 1
    return redirect('store:panier')

def augmenter(request, panier_id):
    item= Panier.objects.get(pk= panier_id)
    item.quantity += 1
    item.save()

    return redirect('store:panier')

def diminuer(request, panier_id):
    item= Panier.objects.get(pk= panier_id)
    if item.quantity > 1:
         item.quantity -= 1
         item.save()
    else:
        item.delete()

    return redirect('store:panier')

def supprimer(request, panier_id):
    panier= Panier.objects.get(pk= panier_id)
    panier.delete()
    return redirect('store:panier')


