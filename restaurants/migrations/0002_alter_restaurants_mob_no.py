# Generated by Django 3.2.4 on 2021-09-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='mob_no',
            field=models.CharField(max_length=10),
        ),
    ]
