# Generated by Django 5.1.6 on 2025-05-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_seller_app', '0002_seller_bank_account_number_seller_bank_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='bank_account_number',
            field=models.CharField(blank=True, help_text='Account Bank Number.', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='bank_name',
            field=models.CharField(blank=True, help_text='Name for Bank.', max_length=100, null=True),
        ),
    ]
