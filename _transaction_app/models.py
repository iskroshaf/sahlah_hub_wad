# _transaction_app/models.py
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class Transaction(models.Model):

    # ── ENUMS ────────────────────────────────────────────────
    class Gateway(models.TextChoices):
        TOYYIBPAY = "toyyibpay", "ToyyibPay"
        # tambah gateway lain di sini jika perlu

    class Status(models.TextChoices):
        PENDING  = "PENDING",  "Pending"
        SUCCESS  = "SUCCESS",  "Success"
        FAILED   = "FAILED",   "Failed"

    # ── FIELDS ───────────────────────────────────────────────
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="transactions",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )

    reference = models.UUIDField(               # unik sepanjang masa
        default=uuid.uuid4, editable=False, unique=True
    )

    bill_code = models.CharField(               # BillCode ToyyibPay
        max_length=50, blank=True, null=True, db_index=True
    )

    gateway = models.CharField(
        max_length=20,
        choices=Gateway.choices,
        default=Gateway.TOYYIBPAY,
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=8, choices=Status.choices,
        default=Status.PENDING, db_index=True
    )

    paid_at   = models.DateTimeField(null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    # ── MODEL META ───────────────────────────────────────────
    class Meta:
        ordering = ["-created_at"]
        indexes  = [
            models.Index(fields=["bill_code"]),
            models.Index(fields=["status"]),
        ]

    # ── STR  ────────────────────────────────────────────────
    def __str__(self):
        code = self.bill_code or str(self.reference)[:8]
        return f"{code} ({self.status})"

    # ── HELPERS ─────────────────────────────────────────────
    def mark_success(self, bill_code: str | None = None):
        """ Tandai transaksi berjaya & set masa bayaran. """
        self.status  = self.Status.SUCCESS
        self.paid_at = timezone.now()
        if bill_code:
            self.bill_code = bill_code
        self.save(update_fields=["status", "paid_at", "bill_code", "updated_at"])

    def mark_failed(self):
        """ Tandai transaksi gagal. """
        self.status = self.Status.FAILED
        self.save(update_fields=["status", "updated_at"])
