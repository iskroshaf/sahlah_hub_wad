# Generated by Django 5.1.6 on 2025-06-17 16:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_transaction_app', '0003_alter_transaction_amount_alter_transaction_bill_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_reference',
            new_name='reference',
        ),
        migrations.AddField(
            model_name='transaction',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='bill_code',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='gateway',
            field=models.CharField(choices=[('toyyibpay', 'ToyyibPay')], default='toyyibpay', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], db_index=True, default='PENDING', max_length=8),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['bill_code'], name='Dtransactio_bill_co_04aa9c_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['status'], name='Dtransactio_status_ac5c2c_idx'),
        ),
    ]
