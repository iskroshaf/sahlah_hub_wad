from decimal import Decimal
from django.db.models import F, Sum
from django.core.exceptions import ValidationError
from .models import Cart, CartItem
from _product_app.models import ProductVariant

# ---------------- helper: troli aktif ----------------
def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        skey = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=skey)
    return cart

# ---------------- tambah item ----------------
def add_to_cart(request, variant_id: int, qty: int):
    cart    = _get_cart(request)
    variant = ProductVariant.objects.get(pk=variant_id)

    if qty < 1:
        raise ValidationError("Kuantiti minimum ialah 1.")
    if qty > variant.variant_quantity:               # ← ganti di sini
        raise ValidationError("Stok tak mencukupi.")

    item, created = CartItem.objects.get_or_create(
        cart=cart, variant=variant, defaults={'quantity': qty}
    )
    if not created:
        CartItem.objects.filter(pk=item.pk).update(quantity=F('quantity') + qty)

# ---------------- set kuantiti tepat ----------------
def set_quantity(request, variant_id: int, qty: int):
    cart = _get_cart(request)
    item = CartItem.objects.filter(cart=cart, variant_id=variant_id).first()
    if not item:
        raise ValidationError("Item tidak wujud dalam troli.")

    if qty <= 0:
        item.delete()
        return None
    if qty > item.variant.variant_quantity:          # ← dan di sini
        raise ValidationError("Stok tak mencukupi.")

    item.quantity = qty
    item.save()
    return item

# ---------------- utiliti paparan ----------------
def get_items(request):
    cart = _get_cart(request)
    return (CartItem.objects
            .filter(cart=cart)
            .select_related('variant__product__shop'))

def cart_total(request):
    cart = _get_cart(request)
    agg = (CartItem.objects
           .filter(cart=cart)
           .aggregate(total=Sum(F('quantity') * F('variant__variant_price'))))
    return agg['total'] or Decimal('0.00')
