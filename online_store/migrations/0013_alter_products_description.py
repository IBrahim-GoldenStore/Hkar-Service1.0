# Generated by Django 5.0.6 on 2024-08-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0012_alter_products_image1_alter_products_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.TextField(default='...sur GoldenStore', verbose_name='Description'),
        ),
    ]
