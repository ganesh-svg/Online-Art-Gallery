# Generated by Django 3.0.5 on 2020-10-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_slug',
            field=models.SlugField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
