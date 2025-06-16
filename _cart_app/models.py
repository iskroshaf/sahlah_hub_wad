from django.conf import settings
from django.db import models
from _product_app.models import ProductVariant   

class Cart(models.Model):
    user        = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE,
                                 related_name='items')
    variant  = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cart', 'variant')
        db_table = "cart"

