# _transaction_app/models.py

import uuid
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED  = "FAILED",  "Failed"

    user                  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="transactions",   # unik bagi Transaction.app
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    transaction_reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    bill_code             = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="ToyyibPay BillCode",
    )
    gateway               = models.CharField(
        max_length=50,
        default="toyyibpay",
    )
    amount                = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    status                = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at            = models.DateTimeField(auto_now_add=True)
    updated_at            = models.DateTimeField(auto_now=True)

    def __str__(self):
        code = self.bill_code or self.transaction_reference
        return f"{code} ({self.status})"
