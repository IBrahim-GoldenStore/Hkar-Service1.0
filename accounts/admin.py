from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Messages_site)
class ContactAdmin(admin.ModelAdmin):
    list_display=('nom','message','e_mails')

