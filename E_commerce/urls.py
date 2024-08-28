"""
URL configuration for E_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static  # son importation est necessaire pour l'ajout du fichier media

urlpatterns = [
    path("",lambda request: redirect('H.kar-Service/',permanent= False)),
    path('onlineStore/', admin.site.urls),
    path('H.kar-Service/',include('online_store.urls_store')),
    path('accounts/',include('accounts.urls_account'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # ajout du fichier media au chemin
