# _shop_app/utils.py
from decimal import Decimal
from types   import SimpleNamespace
from _delivery_app.models import DeliveryMethod    

def get_shipping_options_for_shop(shop):
    
    # 1. Kedai guna harga tersuai
    if shop.delivery_price_type == "custom":
        fee = Decimal(shop.shop_delivery_fee or 0)
        return [], None, fee

    # 2. Cari ShopDelivery aktif
    qs = (
        shop.shopdelivery_set
            .select_related("method")
            .filter(method__is_active=True)
            .order_by("method__name")
    )

    # 3. Fallback: guna semua DeliveryMethod aktif
    if not qs.exists():
        qs = [
            SimpleNamespace(
                method          = dm,
                extra_surcharge = Decimal("0.00"),
                id              = f"dm-{dm.id}",
            )
            for dm in DeliveryMethod.objects.filter(is_active=True).order_by("name")
        ]

    # 4. Kalau masih kosong, pulangkan nilai neutral
    if not qs:
        return [], None, Decimal("0.00")

    sd0  = qs[0]
    fee0 = sd0.method.base_price + sd0.extra_surcharge
    return qs, sd0, fee0
