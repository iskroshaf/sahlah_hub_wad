# Generated by Django 5.1.6 on 2025-06-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_shop_app', '0003_alter_shop_shop_delivery_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='shop_delivery_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
