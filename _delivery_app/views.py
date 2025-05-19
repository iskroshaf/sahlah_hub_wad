# _delivery_app/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeliveryMethodForm
from .models import DeliveryMethod

def delivery_list_view(request):
    theme = "admin_seller_theme"
    methods = list(DeliveryMethod.objects.all())

    # Senarai warna untuk active methods
    colors = ["success", "primary", "warning", "info"]
    for idx, m in enumerate(methods):
        # kalau tak active, pakai secondary
        if not m.is_active:
            m.color = "secondary"
        else:
            m.color = colors[idx % len(colors)]

    context = {
        "methods": methods,
        "title":   "Delivery Methods",
        "theme":   theme,
    }
    return render(request, "_delivery_app/delivery_list.html", context)

def delivery_create_view(request):
    theme = "admin_seller_theme"

    if request.method == "POST":
        form = DeliveryMethodForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery method created.")
            return redirect("delivery_list")
    else:
        form = DeliveryMethodForm()

    context = {
        "form":  form,
        "title": "Add Delivery Method",
        "theme": theme,
    }
    return render(request, "_delivery_app/delivery_form.html", context)

def delivery_update_view(request, pk):
    theme = "admin_seller_theme"
    method = get_object_or_404(DeliveryMethod, pk=pk)

    if request.method == "POST":
        form = DeliveryMethodForm(request.POST, instance=method)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery method updated.")
            return redirect("delivery_list")
    else:
        form = DeliveryMethodForm(instance=method)

    context = {
        "form":  form,
        "title": "Edit Delivery Method",
        "theme": theme,
    }
    return render(request, "_delivery_app/delivery_form.html", context)
