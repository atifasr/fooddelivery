# Generated by Django 3.2.5 on 2021-08-02 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_placedorder_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='placedorder',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]
