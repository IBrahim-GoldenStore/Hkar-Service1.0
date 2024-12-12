from . import views
from django.urls import path

app_name='store'


urlpatterns = [
    path('', views.index, name='index'),
    path('nos_produits/', views.produit, name='prods'),
    path('achat_effectuer/',views.buy,name='success'),
    #pour ajouter des jetons automatiquement  path('jeton/', views.jeton, name='jeton'),
    # panier url
    path('panier/', views.panier, name='panier'),
    path('panier_add/<int:article_id>/',views.ajouter, name ='ajout'),
    path('panier/augmenter/<int:panier_id>', views.augmenter, name='plus'),
    path('panier/diminuer/<int:panier_id>', views.diminuer, name='moins'),
    path('panier/supprimer/<int:panier_id>', views.supprimer, name='supprimer'),
    path('categorie/<str:category_name>/',views.trend,name='trend'),
    path('<slug:id_prod>/',views.article, name='article'), # recuperation par slug on defint tjrs d'aborb le type ensuite un variable a son nom(ex: <slug:id_prod>)
]
