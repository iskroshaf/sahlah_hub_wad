# _order_app/models.py

from django.db import models
from django.conf import settings

from _delivery_app.models import DeliveryMethod
from _shop_app.models import Shop
from _transaction_app.models import Transaction
from _customer_app.models import ShippingAddress 




class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",      # unik bagi Order ↔ User
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    session_key = models.CharField(max_length=40, blank=True)

    # Hubungan satu-ke-satu ke Transaction, bersifat optional
    transaction = models.OneToOneField(
        Transaction,
        related_name="order",       # unik bagi Transaction ↔ Order
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    # Boleh NULL kerana kita simpan courier per-kedai di OrderShipping
    shipping_method = models.ForeignKey(
        DeliveryMethod,
        related_name="orders_with_method",  # unik bagi DeliveryMethod ↔ Order
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    shipping_address = models.ForeignKey(
        ShippingAddress,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders',
    )
    shipping_fee  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_products = models.DecimalField(max_digits=10, decimal_places=2)

    eta_min = models.PositiveIntegerField(default=0)
    eta_max = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.transaction and self.transaction.bill_code:
            return f"Order #{self.pk} – {self.transaction.bill_code}"
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",        # unik bagi Order ↔ OrderItem
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        "_product_app.ProductVariant",
        related_name="order_items",  # unik bagi ProductVariant ↔ OrderItem
        on_delete=models.PROTECT
    )
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant} × {self.quantity}"


class OrderShipping(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="shippings",   # unik bagi Order ↔ OrderShipping
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop,
        related_name="order_shippings",  # unik bagi Shop ↔ OrderShipping
        on_delete=models.PROTECT
    )
    method = models.ForeignKey(
        DeliveryMethod,
        related_name="shipping_entries",  # unik bagi DeliveryMethod ↔ OrderShipping
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ("order", "shop")

    def __str__(self):
        return f"{self.shop} – {self.method} (RM{self.fee})"
