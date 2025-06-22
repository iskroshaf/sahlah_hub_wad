# _order_app/services.py
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from _product_app.models import ProductVariant
from _product_app.signals import clamp_cart_items, update_parent_stock   # import fungsi terus

@transaction.atomic
def lock_and_deduct_stock(order):
    variant_ids = [it.variant_id for it in order.items.select_related('variant')]

   
    variants = ProductVariant.objects.select_for_update().filter(id__in=variant_ids)
    v_map = {v.id: v for v in variants}

    
    for item in order.items.all():
        v = v_map[item.variant_id]
        if v.variant_quantity < item.quantity:
            raise ValidationError(
                f"Stok {v} tinggal {v.variant_quantity}, pesanan perlukan {item.quantity}"
            )

   
    for item in order.items.all():
        (
            ProductVariant.objects
            .filter(pk=item.variant_id)
            .update(variant_quantity=F('variant_quantity') - item.quantity)
        )

    # panggil helper supaya pasti jalan
    for item in order.items.all():
        v = v_map[item.variant_id]
        v.refresh_from_db()             # baca stok terkini
        update_parent_stock(v.product)
        clamp_cart_items(ProductVariant, v)   # manual trigger
