# Generated by Django 5.0.6 on 2024-08-09 19:59

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0014_lieu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Numéro de téléphone(8 caracteres)'),
        ),
    ]
