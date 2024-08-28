from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display= ('name','price','quantity','category','top_category','description','image')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display= ('user','number','adresse','name_and_quantity','montant','statut','date')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display= ('name',)

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display= ('name','quantity','price',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('name','image',)

@admin.register(Livraison)
class Livraison(admin.ModelAdmin):
    list_display= ('option',)

@admin.register(Lien)
class Lien(admin.ModelAdmin):
    list_display= ('name','url')