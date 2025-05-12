from django.shortcuts import get_object_or_404, redirect, render

from _shop_app.forms import ShopForm, ShopUpdateForm
from _shop_app.models import Shop
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def shop_register_view(request):
    title = "Shop Register"
    theme = "admin_seller_theme"
    storage = messages.get_messages(request)   
    storage.used = True          
    form = ShopForm()
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user.seller
            shop = form.save(commit=False)
            shop.seller = seller
            shop.save()
                          
            messages.success(request, "Shop registered successfully!")
            return redirect("shop_list") 
        else:
            messages.error(request, "Please fix the errors in the form.")
           
    context = {
        "title": title,
        "theme": theme,
        "form": form,
    }
    return render(request, "_shop_app/shop_register.html", context)


def shop_list_view(request):
    title = "My Shop"
    theme = "admin_seller_theme"
    seller = request.user.seller
    shops = Shop.objects.filter(seller=seller)
    context = {
        "title": title,
        "theme": theme,
        "shops": shops,
    }
    return render(request, "_shop_app/shop_list_seller.html", context)


def shop_dashboard_view(request, pk):
    title = "Shop Dashboard"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)
    context = {
        "title": title,
        "shop": shop,
        "theme": theme,
    }
    return render(request, "_shop_app/shop_dashboard.html", context)

def seller_edit_shop(request, shop_id):
    title = "Shop Dashboard"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=shop_id, seller=request.user.seller)

    if request.method == "POST":

        storage = messages.get_messages(request)   
        storage.used = True 
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop updated successfully.")
            return redirect("shop_list")
        else:
            # if not form.is_valid():
            #      print("FORM ERRORS:", form.errors)           # ← cetak ke console/server log
            #      for field, errors in form.errors.items():     # ← kalau nak detail
            #         for e in errors:
            #             print(f"- {field}: {e}")
            # render semula halaman list dengan ralat & id kedai
            shops = Shop.objects.filter(seller=request.user.seller)
            return render(
                 request,
            "_shop_app/shop_list_seller.html",
            {
                "title": title,          # <-- TAMBAH
                "theme": theme,          # <-- TAMBAH
                "shops": shops,
                "error_shop_id": shop_id,
                "edit_form": form,
            },
            )

    return redirect("shop_list")