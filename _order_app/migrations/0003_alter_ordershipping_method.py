# Generated by Django 5.1.6 on 2025-06-16 00:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_delivery_app', '0002_alter_deliverymethod_table_alter_shopdelivery_table'),
        ('_order_app', '0002_remove_order_shipping_surcharge_alter_order_eta_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordershipping',
            name='method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='_delivery_app.deliverymethod'),
        ),
    ]
