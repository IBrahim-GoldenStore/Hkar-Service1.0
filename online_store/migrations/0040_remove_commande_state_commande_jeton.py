# Generated by Django 5.0.6 on 2024-11-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("online_store", "0039_commande_state"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commande",
            name="state",
        ),
        migrations.AddField(
            model_name="commande",
            name="jeton",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="jeton"
            ),
        ),
    ]