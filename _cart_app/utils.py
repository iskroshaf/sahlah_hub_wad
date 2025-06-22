# _cart_app/utils.py
from django.contrib import messages

def clamp_cart(request, cart):
    """Balik True kalau ada perubahan kuantiti."""
    changed = False
    for item in cart.items.select_related("variant"):
        avail = item.variant.variant_quantity
        if avail == 0:
            item.delete()
            changed = True
        elif item.quantity > avail:
            item.quantity = avail
            item.save(update_fields=["quantity"])
            changed = True

    if changed:
        if cart.items.exists():
            messages.warning(
                request,
                "Beberapa kuantiti dikemas kini kerana stok berubah. "
                "Sila semak troli semula."
            )
        else:
            messages.error(request, "Semua item dalam troli habis stok.")
    return changed
