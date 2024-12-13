# Generated by Django 5.0.6 on 2024-07-31 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_store', '0009_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='products',
            name='image1',
            field=models.ImageField(default='img/deflaut1', null=True, unique=True, upload_to='./img', verbose_name='image 2'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image2',
            field=models.ImageField(default='img/deflaut2', null=True, unique=True, upload_to='./img', verbose_name='image 3'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image3',
            field=models.ImageField(default='img/deflaut3', null=True, unique=True, upload_to='./img', verbose_name='image 4'),
        ),
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantité'),
        ),
    ]
