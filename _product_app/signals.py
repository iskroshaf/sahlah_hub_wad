# _product_app/signals.py
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

from _product_app.models import Product, ProductVariant


# ── kemas kini stok global produk ───────────────────────────────
def update_parent_stock(product):
    total = product.variants.aggregate(
        total_qty=models.Sum('variant_quantity')
    )['total_qty'] or 0
    Product.objects.filter(pk=product.pk).update(product_quantity=total)


@receiver(post_save, sender=ProductVariant)
def on_variant_save(sender, instance, **kwargs):
    update_parent_stock(instance.product)


@receiver(post_delete, sender=ProductVariant)
def on_variant_delete(sender, instance, **kwargs):
    update_parent_stock(instance.product)


# ── clamp troli apabila stok varian berubah ─────────────────────
@receiver(post_save, sender=ProductVariant)
def clamp_cart_items(sender, instance, **kwargs):
    """Potong semua CartItem yang melebihi stok baharu."""
    CartItem = apps.get_model('_cart_app', 'CartItem')     # lazy import
    qs = CartItem.objects.filter(
        variant=instance, quantity__gt=instance.variant_quantity
    )
    if instance.variant_quantity == 0:
        qs.delete()
    else:
        qs.update(quantity=instance.variant_quantity)
