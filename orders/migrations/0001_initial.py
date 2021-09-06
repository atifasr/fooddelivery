# Generated by Django 3.2.4 on 2021-09-06 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customers')),
            ],
        ),
        migrations.CreateModel(
            name='PlacedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('estimated_delivery_time', models.TimeField(blank=True, null=True)),
                ('actual_delivery_time', models.TimeField(blank=True, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(blank=True, null=True)),
                ('city', models.CharField(max_length=25)),
                ('building', models.CharField(blank=True, max_length=25)),
                ('zip_code', models.CharField(max_length=25)),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('razor_pay_signature', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(max_length=25)),
                ('mob_no', models.CharField(max_length=20, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=25)),
                ('time', models.TimeField(auto_now=True)),
                ('order', models.ManyToManyField(to='orders.PlacedOrder')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('size', models.CharField(blank=True, max_length=25)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menus.menuitem')),
                ('ordereditem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.placedorder')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField()),
                ('is_req', models.BooleanField()),
                ('is_complaint', models.BooleanField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customers')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.placedorder')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('size', models.CharField(max_length=25)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.cart')),
                ('menu_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.menuitem')),
            ],
        ),
    ]