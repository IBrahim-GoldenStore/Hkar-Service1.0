from django.urls import path
from. import views

app_name = 'account'

urlpatterns = [
    path('Connexion/',views.connexion , name='login'),
    path('Deconnexion/',views.deconnexion , name='logout'),
    path('Compte/',views.compte , name='register'),
    path("Nous_contactez/", views.contacts , name="cont")
]
