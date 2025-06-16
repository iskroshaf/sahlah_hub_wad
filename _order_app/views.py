from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
from .models import Order

def order_detail(request, order_id):
    """
    Papar ringkasan pesanan selepas checkout.
    Boleh perkemas kemudian (status, senarai item, dsb.).
    """
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_detail.html', {'order': order})