# _order_app/models.py
from django.db import models
from django.conf import settings
from _delivery_app.models import DeliveryMethod
from _shop_app.models import Shop


class Order(models.Model):
    user          = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    session_key   = models.CharField(max_length=40, blank=True)

    # Boleh NULL kerana kita simpan courier per-kedai di OrderShipping
    shipping_method = models.ForeignKey(
        DeliveryMethod, null=True, blank=True, on_delete=models.SET_NULL
    )

    shipping_fee  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_products = models.DecimalField(max_digits=10, decimal_places=2)

    eta_min = models.PositiveIntegerField(default=0)
    eta_max = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    variant    = models.ForeignKey("_product_app.ProductVariant", on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant} × {self.quantity}"


class OrderShipping(models.Model):
    """Satu baris bagi setiap kedai dalam pesanan."""
    order  = models.ForeignKey(Order, related_name="shippings", on_delete=models.CASCADE)
    shop   = models.ForeignKey(Shop, on_delete=models.PROTECT)
    method = models.ForeignKey(
                 DeliveryMethod,
                 on_delete=models.SET_NULL,
                 null=True,        # ✅
                 blank=True        # ✅
             )
    fee    = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ("order", "shop")

    def __str__(self):
        return f"{self.shop} – {self.method} (RM{self.fee})"
