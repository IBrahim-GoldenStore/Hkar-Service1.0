# Generated by Django 5.0.6 on 2024-11-17 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("online_store", "0037_jeton"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jeton",
            name="token",
            field=models.IntegerField(
                blank=True, default=1, null=True, verbose_name="Jeton"
            ),
        ),
    ]
