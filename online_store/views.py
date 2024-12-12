from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# fonctions utiles
def send_letter(name,user_email,subject: str,detail:list,typeof:int,montant,livraison):
    context={
        'livraison':livraison,
        'username': name,
        'liste':detail,
        'type': typeof,
        'montant': sum(montant),
        'contact':'hkarservice.team@gmail.com'
    }
    email= render_to_string('onlineStore/email_template.html',context)
    email_brute= strip_tags(email)
    msg= EmailMultiAlternatives(subject,email_brute,'',[user_email,'goldensotrebox@gmail.com'])
    msg.attach_alternative(email,"text/html")
    msg.send()

def send_commande(name,email,number,localisation,articles,type1,montant,livraison):
        subject= "Commande de la part de "+name+'.'
        context={
            'livraison':livraison,
            'name': name,
            'email': email,
            'number': number,
            'liste': articles,
            'localisation': localisation,
            'type': type1,
            'montant': sum(montant),
        }
        email= render_to_string('onlineStore/commande.html',context)
        email_brute= strip_tags(email)
        msg= EmailMultiAlternatives(subject,email_brute,'',receivers())
        msg.attach_alternative(email,"text/html")
        msg.send()


def fiche(produits):
    category_list= set() # set() cree un ensemble sans doublon
    for produit in produits:
        if produit.category.name:
            target_category= Category.objects.get(name= produit.category.name)
            category_list.add(target_category)

    category_list= list(category_list)
    shuffle(category_list)
    return category_list

def FooterCollaborator():
    box=list(NosCollaborateurs.objects.all())
    shuffle(box)
    return_box=[]
    if len(box)>5:
       for i in range(0,len(box)):
           return_box.append(box[i])

    return return_box


def FooterCategory():
    category= Category.objects.all()
    category=list(category)
    shuffle(category)
    return_category=[]
    for i in range(0,6):
        return_category.append(category[i])

    return return_category

def FooterArticles():
    produits= Products.objects.filter(top_category=1)
    produits=list(produits)
    shuffle(produits)
    return_category=[]
    for i in range(0,6):
        return_category.append(produits[i])

    return return_category


def receivers():
    receiver= User.objects.filter(is_staff=True)
    emails= receiver.values_list('email',flat=True)
    return emails

def CreateCommande(liste,number,adresse,user,montant):
    statue= Statue.objects.get(statue='En attente..')
    for item in liste:
        detail=f"Panier de: {user.username},\n Total du panier: {montant},\n Article: {item.article.name}"
        new=Commande.objects.create(user=user,name=None,number=number,adresse=adresse,article= item.article,quantity=item.quantity,montant=item.article.price,details=detail+item.article.name,statue=statue)
        new.save()

def error(request,context):
    return render(request,'onlineStore/error.html',{'context': context})


# fonction utiles

# Create your views here.

 # recuperation des differents produits
def index(request):
    category= Category.objects.all()
    produit_list= Products.objects.filter(top_category=1)
    search= request.GET.get('contain') # recuperation de la valeur via son nom dans le formulaire
    if search !="" and search is not None:# verification
        produit_list= Products.objects.filter(name__icontains=search.strip())  # flitrez les donnees selon la valeur rentrez notez que <__icontains> s'utilise sur le champs qui doit etre verifie sans intermediaire du point

    context= {
        'category': category,
        'category_list': fiche(produit_list),
        'produit_list': produit_list,
        'footer_category': FooterCategory(),
        'footer_articles': FooterArticles(),
        'collaborateurs': FooterCollaborator()
    }

    return render(request, 'onlineStore/index.html',context)


def produit(request):
    produit_list= Products.objects.all()

    search= request.GET.get('contain') # recuperation de la valeur via son nom dans le formulaire
    if search !="" and search is not None: # verification
        produit_list= Products.objects.filter(name__icontains=search.strip())  # flitrez les donnees selon la valeur rentrez notez que <__icontains> s'utilise sur le champs qui doit etre verifie sans intermediaire du point

    context={
        'category_list': fiche(produit_list),
        'produit_list': produit_list,
        'footer_category': FooterCategory(),
        'footer_articles': FooterArticles(),
        'collaborateurs': FooterCollaborator()

    }

    return render(request,'onlineStore/produits.html',context)

def trend(request, category_name):
    category= Category.objects.get(name=category_name)
    category_list=set()
    category_list.add(category)
    produit_list= Products.objects.filter(category= category.id)

    return render(request, 'onlineStore/produits.html',{'produit_list': produit_list,'category_list':category_list,'footer_articles': FooterArticles(),'footer_category': FooterCategory(),'collaborateurs': FooterCollaborator()})

# recuperation d'un article

def buy(request):
       return render(request,'onlineStore/success.html',{})

def article(request,id_prod):
    article= get_object_or_404(Products, slug= id_prod)
    livraison= article.livraison
    token= False
    free_offer= False
    statue= Statue.objects.get(statue="En attente..")
    user = request.user   # recupere l'utilsteur actuellement connectez
    if article.quantity > 0:
        if user.is_authenticated:
            #jeton= Jeton.objects.get(user=user)
            #free_offer= Livraison.objects.get(option__icontains='gratuit')
            #token= jeton.token
            #if token > 0:
                #livraison=free_offer
            if request.method == "POST":
                form = Panier_form(request.POST)
                if form.is_valid():
                    # recupreration des donnees depuis un formulaire
                    name =  user.username
                    number= form.cleaned_data['number']
                    adress= form.cleaned_data['adresse']
                    email=  user.email

                    # envois d emai
                    #sujet= 'Nouvelle commande de la part de {}'.format(name)
                    #contenu=  "Numero telephonique: {} ,\n E_mail: {},\n Produit &  Quantite: {},\n Montant du Commande: {},\n Localisation: {},\n Achat directe,".format(number,email,article.name,article.price,adress)
                    send_commande(name,email,number,adress,[article],1,[],livraison)
                    send_letter(name,email,'Achat sur Hkar-Service.',[article],1,[],livraison)

                    detail= "Achat directe. \n"+ "Nom de l'article :" + article.name
                    Commande.objects.create(user= user,number= number, adresse= adress,article= article,quantity=1,montant= article.price,details=detail,statue=statue,jeton=False)

                    return redirect('store:success')
                else:
                    return error(request,'Assurez-vous que vôtre numero est valide!!')
            else:
                form= Panier_form()
        else:
            if request.method == "POST":
                form = BuyForm(request.POST)
                if form.is_valid():
                    # recupreration des donnees depuis un formulaire
                    name =  form.cleaned_data['name']
                    number= form.cleaned_data['number']
                    adress= form.cleaned_data['adresse']
                    email=  form.cleaned_data['email']

                    # envois d emai
                    #sujet= 'Nouvelle commande de la part de {}'.format(name)
                    #contenu=  "Numero telephonique: {} ,\n,\n Produit &  Quantite: {},\n Montant du Commande: {},\n Localisation: {},\n Achat directe,".format(number,article.name,article.price,adress)
                    send_commande(name,email,number,adress,[article],1,[],livraison)
                    send_letter(name,email,'Achat sur Hkar-Service.',[article],1,[],livraison)

                    detail= "Achat directe. \n"+ "Nom de l'article :" + article.name
                    Commande.objects.create(user=None,name=name,number= number, adresse= adress,article= article,quantity=1,montant= article.price,details=detail,statue=statue,jeton=False)

                    return redirect('store:success')
                else:
                    return error(request,'Assurez-vous que vôtre numero est valide!!')
            else:
                form= BuyForm()
    else:
        return error(request,'Article indisponible en stock')

    return render(request, "onlineStore/article.html",{"article": article,'token':token,'free_offer':free_offer,'form':form,'couleur': Color.objects.get(name='Non disponible')})

# traitement du panier
@login_required
def panier(request):
    panier =  Panier.objects.filter(user= request.user)
    liste=[]
    if panier is not None:
        commande_list= []
        montant=[]                    # Creation d'une table vide qui vas contenir tout le montant de chaque produit
        for item in panier:           # parcourir la liste d'objets "panier" tout en associant chaque objet a item
            montant.append(item.quantity*item.price)    #Grace a la methode append() nous recuperons le montant(quantite x prix) de chaque item et l'ajoutez au table montant
            commande_list.append((item.name,item.quantity))
            liste.append(item)
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
                #sujet= 'Nouvelle commande de la part de {}'.format(name)
                #contenu=  "Numero telephonique: {} ,\n E_mail: {},\n Produit &  Quantite: {},\n Montant du Commande: {},\n Localisation: {},\n Via le panier".format(number,email,commande_list,sum(montant),adress,)
                send_commande(name,email,number,adress,liste,0,montant,False)
                send_letter(name,email,'Achat sur Hkar-Service.',liste,0,montant,False)

                CreateCommande(panier,number,adress,user,sum(montant))
                panier.delete()
                return redirect('store:success')
            else:
                return error(request,'Assurez-vous que vôtre numero est valide!!')
        else:
            form= Panier_form()

        return render(request, 'onlineStore/panier.html', {'panier': panier,'montant':sum(montant),'form': form})     # Nous retournons la table montant tout en faisant la somme de ces elements ( sum() )
    else:
        return render(request, 'onlineStore/panier.html', {'panier': '','montant':sum(montant),'form': form})     # Nous retournons la table montant tout en faisant la somme de ces elements ( sum() )


@login_required
def ajouter(request, article_id):
    produit= Products.objects.get(pk= article_id)
    panier, created= Panier.objects.get_or_create(name= produit.name,price= produit.price,user= request.user,article=produit)
    if not created:
        panier.quantity += 1
    return redirect('store:panier')

def augmenter(request, panier_id):
    item= Panier.objects.get(pk= panier_id)
    article= Products.objects.get(name=item.article.name)
    if article.quantity > item.quantity:
        item.quantity += 1
        item.save()
        return redirect('store:panier')
    else:
       return error(request,  'Quantité indisponible en stock')

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

@receiver(pre_save,sender=Commande)
def update(sender,instance,*args, **kwargs):
    article= Products.objects.get(name=instance.article.name)
    statue= Statue.objects.get(statue='Effectuer.')

    try:
        user = User.objects.get(username=instance.user.username)
        if user.jeton.token > 0 and instance.jeton:
            user.jeton.token -=1
            user.jeton.save()
    except:
        pass

    if instance.statue == statue:
        if article.quantity > 0:
            article.quantity -= instance.quantity
            article.save()

@receiver(pre_save,sender=Products)
def updateProduct(sender,instance,*args, **kwargs):
    if instance.quantity == 0:
        sujet= "Plus de stock disponible pour l'article "+instance.name
        message= "Le stock de l'article "+instance.name+" est épuisé. \n Veuillez le supprimer ou mettre à jour le stock le plus rapidement possible. \n Bonne journée/Soirée Mr"
        send_mail(sujet,message,'',receivers())

#@login_required
#def jeton(request):
    #user= User.objects.all()
    #for i in user:
        #try:
            #Jeton.objects.create(user=i,token=0)
        #except:
            #pass

    #return redirect('store:index')
