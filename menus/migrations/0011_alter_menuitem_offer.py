# Generated by Django 3.2.4 on 2021-09-04 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0010_alter_offer_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='offer',
            field=models.ManyToManyField(blank=True, to='menus.Offer'),
        ),
    ]