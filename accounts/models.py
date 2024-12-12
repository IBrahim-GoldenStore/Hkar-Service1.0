from django.db import models

# Create your models here.
class Messages_site(models.Model):
    nom= models.CharField(max_length=50, verbose_name='Message de Mr/Mme',unique=False)
    e_mails= models.EmailField(max_length=30, verbose_name="E-mail",unique=False)
    message= models.TextField(verbose_name="Message")

    def __str__(self):
        return self.message

from django.contrib.auth.models import User
class Profil(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    jeton= models.PositiveIntegerField(verbose_name="Jeton",default=0)
    code= models.CharField(max_length=9,unique=True,verbose_name="Code Promo")
    statut= models.CharField(max_length=15,verbose_name="Statut",null=True,blank=True)


    def save(self,*args, **kwargs):
        if not self.code:
            self.code=make_code()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name='Profil'
        verbose_name_plural= 'Profils'

import secrets
import string
def make_code():
    choices= string.ascii_uppercase+string.digits
    for_code= ''
    for _ in range(0,9):
        for_code+=secrets.choice(choices)

    return for_code