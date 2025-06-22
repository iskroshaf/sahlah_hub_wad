from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from _customer_app.models import ShippingAddress
from .models import Order

def order_detail(request, order_id):
    
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_review(request, order_id):
    theme = "customer_theme"
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    alamat_list = ShippingAddress.objects.filter(user=request.user)

    if request.method == "POST":
        addr_id = request.POST.get("alamat_id")
        if addr_id:
            order.shipping_address_id = addr_id
            order.save()
          
            return redirect('payment-create', order_id=order.id)

    return render(request, '_order_app/order_review.html', {
        'theme': 'customer_theme',
        'order': order,
        'alamat_list': alamat_list,  
    })