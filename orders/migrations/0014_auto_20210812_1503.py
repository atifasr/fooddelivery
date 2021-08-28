# Generated by Django 3.2.5 on 2021-08-12 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0010_alter_offer_options'),
        ('orders', '0013_auto_20210812_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='ordered_item',
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.cart'),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='menu_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.menuitem'),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='size',
            field=models.CharField(default='large', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]