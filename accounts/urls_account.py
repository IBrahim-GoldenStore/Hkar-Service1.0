from django.urls import path
from. import views

app_name = 'account'

urlpatterns = [
    path('Connexion/',views.connexion , name='login'),
    path('Profil',views.profil_view,name='profil'),
    path('Deconnexion/',views.deconnexion , name='logout'),
    path('Compte/',views.compte , name='register'),
    path("Nous_contactez/", views.contacts , name="cont"),
    path('Inscription_réussi/',views.success,name='success'),
    path("Password_reset/",views.send_reset_email,name='reset_password'),
    path("new_password/<uid>/<token>/", views.set_new_password, name="setpassword")
]
