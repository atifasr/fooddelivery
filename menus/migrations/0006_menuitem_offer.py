# Generated by Django 3.2.5 on 2021-08-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='offer',
            field=models.ManyToManyField(to='menus.Offer'),
        ),
    ]
