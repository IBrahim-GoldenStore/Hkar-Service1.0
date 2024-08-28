from django.db import models

# Create your models here.
class Messages_site(models.Model):
    nom= models.CharField(max_length=50, verbose_name='Message de Mr/Mme',unique=False)
    e_mails= models.EmailField(max_length=30, verbose_name="E-mail",unique=False)
    message= models.TextField(verbose_name="Message")

    def __str__(self):
        return self.message