import os
from django.db import models
from PIL import Image
from io import BytesIO
from django.dispatch import receiver
from django.db.models.signals import pre_save,pre_delete
from django.core.files import File
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

class Lien(models.Model):
    name= models.CharField(max_length=20,verbose_name="Nom du lien")
    url= models.URLField(blank=True,verbose_name='lien')

    def __str__(self):
        return self.name

class Jeton(models.Model):
    token= models.IntegerField(verbose_name='Jeton',null=True,blank=True,default=1)
    user= models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)


class Color(models.Model):
    name= models.CharField(max_length=15, verbose_name="Couleur disponible")

    class Meta:
        verbose_name= 'Couleur'
        verbose_name_plural= 'Couleurs'

    def __str__(self):
        return self.name

class Livraison(models.Model):
    option= models.CharField(max_length=25, verbose_name='Option disponible' )

    def __str__(self) -> str:
        return self.option

class Category(models.Model):
    name = models.CharField(max_length=20)
    image= models.ImageField(upload_to='./img_category',default='',null=False)

    class Meta:
        verbose_name= 'Categorie'
        verbose_name_plural= 'Categories'

    def __str__(self):
        return self.name

# modele des produits
class Products (models.Model):
    name = models.CharField(max_length=60, unique= True, verbose_name="Nom")
    price = models.FloatField(verbose_name= "Prix", )
    quantity = models.PositiveIntegerField(verbose_name="Quantité", default= 1)
    category= models.ForeignKey(Category,on_delete= models.CASCADE ,null= True, unique=False, verbose_name='categorie')
    top_category= models.BooleanField(verbose_name="Tendance",default=0)
    description= models.TextField(verbose_name="Description", default="...sur Hkar Service")
    image= models.ImageField(upload_to='./img1_pack', verbose_name="image",unique=True,default='')
    image1= models.ImageField(upload_to='./img2_pack', null=True,verbose_name="image 2",blank=True,default='')
    image2= models.ImageField(upload_to='./img3_pack', null=True, verbose_name="image 3",blank=True,default='')
    image3= models.ImageField(upload_to='./img4_pack', null=True, verbose_name="image 4",blank=True,default='')
    color= models.ForeignKey(Color,on_delete= models.DO_NOTHING,default=1)
    slug= models.SlugField(unique=True,default='')
    livraison= models.ForeignKey(Livraison, on_delete= models.CASCADE,default=1)
    class Meta:
        verbose_name="Produit"
        verbose_name_plural="Produits"
        # abstract= True  pour utilser les champs dans d'autre class mais le modele ne sera plus utiliser

    def __str__(self):
        return self.name



 # modele des paniers
class Panier(models.Model):
     name=models.CharField(max_length=23,verbose_name='Nom')
     quantity= models.PositiveIntegerField(verbose_name="Quantite", default=1)
     price = models.FloatField(verbose_name="Prix")
     article = models.ForeignKey(Products, on_delete= models.CASCADE, null= True,)
     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
          return self.name

class Statue(models.Model):
    statue= models.CharField(max_length=15,verbose_name='statue',null=True,default='En attente..')
    class Meta:
        verbose_name= 'Statue'
    def __str__(self):
        return self.statue


class Commande(models.Model):

    user= models.ForeignKey(User, on_delete= models.CASCADE,verbose_name='Auteur',null=True,default=None)
    name= models.CharField(max_length=40,verbose_name='Nom',null=True,blank=True)
    number= PhoneNumberField(verbose_name="Numéro de téléphone",unique= False)
    adresse= models.CharField(max_length=50, verbose_name="Lieu de résidence", unique= False,)
    article= models.ForeignKey(Products,on_delete=models.SET_NULL,default=None,null=True)
    quantity= models.PositiveIntegerField(verbose_name='Quantité de commande',default=0)
    montant= models.FloatField(verbose_name='Montant',default=1,unique=False)
    statue= models.ForeignKey(Statue, on_delete= models.SET_NULL, null=True,default=None)
    details= models.CharField(max_length=100,verbose_name='detail',null=True,blank=True)
    date= models.DateField(auto_now_add=True)
    jeton = models.BooleanField(verbose_name='jeton',null=True,blank=True,default=False,editable=False)

# l'ancien structure
    # user= models.ForeignKey(User, on_delete= models.CASCADE,verbose_name='Auteur',null=True,blank=True)
    # number= PhoneNumberField(verbose_name="Numéro de téléphone",unique= False)
    # adresse= models.CharField(max_length=50, verbose_name="Lieu de résidence", unique= False,)
    # name_and_quantity= models.CharField(max_length=50,verbose_name="Nom & Quantité",unique=False)
    # montant= models.FloatField(verbose_name='Montant',default=1,unique=False)
    # statut= models.CharField(verbose_name='statue',max_length=25,default='En attente.')
    # date= models.DateField(auto_now_add=True)
# l'ancien structure

    class Meta:
        verbose_name="Commande"
        verbose_name_plural="Commandes"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.name


class NosCollaborateurs(models.Model):
    nom= models.CharField(verbose_name="Nom",max_length=20)
    prenom= models.CharField(verbose_name="Prenom",max_length=20)
    phone= PhoneNumberField(verbose_name='Telephone',region='ML')
    business_name= models.CharField(verbose_name="Nom de l'entreprise",max_length=30,null=True,blank=True)

    class Meta:
        verbose_name="Collaborateur"
        verbose_name_plural="Nos Collaborateurs"

    def __str__(self):
        return self.business_name

def compressor(objet_image=None,comp_image=None,filename:str=None):
        img= Image.open(comp_image)
        img= img.convert('RGB')
        img.thumbnail((800,800))
        format='webp'
        img_io= BytesIO()
        img.save(img_io, format=format,quality=80)
        img_file= File(img_io, name=filename+'.'+format)
        if objet_image:
            if os.path.isfile(objet_image.path):
                os.remove(objet_image.path)
        return img_file

@receiver(pre_delete,sender=Products)
def delete_objet(sender,instance,*args, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.image1:
        if os.path.isfile(instance.image1.path):
            os.remove(instance.image1.path)
    if instance.image2:
        if os.path.isfile(instance.image2.path):
            os.remove(instance.image2.path)
    if instance.image3:
        if os.path.isfile(instance.image3.path):
            os.remove(instance.image3.path)

@receiver(pre_save,sender=Products)
def get_inst(sender,instance,*args, **kwargs):
    if instance.pk:
        old_inst = Products.objects.get(pk=instance.pk)
        try:
            if old_inst.image != instance.image:
                instance.image=compressor(old_inst.image,instance.image,instance.name)
            if old_inst.image1 != instance.image1:
                instance.image1=compressor(old_inst.image1,instance.image1,instance.name)
            if old_inst.image2 != instance.image2:
                instance.image2=compressor(old_inst.image2,instance.image2,instance.name)
            if old_inst.image3 != instance.image3:
                instance.image3=compressor(old_inst.image3,instance.image3,instance.name)
        except:
            old_inst=None
    else:
        if instance.image:
            instance.image=compressor(None,instance.image,instance.name)
        if instance.image1:
            instance.image1=compressor(None,instance.image1,instance.name)
        if instance.image2:
            instance.image2=compressor(None,instance.image2,instance.name)
        if instance.image3:
            instance.image3=compressor(None,instance.image3,instance.name)
