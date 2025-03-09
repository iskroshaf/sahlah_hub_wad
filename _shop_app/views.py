from django.shortcuts import get_object_or_404, redirect, render

from _shop_app.forms import ShopForm
from _shop_app.models import Shop


def shop_register_view(request):
    title = "Shop Register"
    theme = "admin_seller_theme"
    form = ShopForm()
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user.seller
            shop = form.save(commit=False)
            shop.seller = seller
            shop.save()
            print("Shop Register Successful")
            return redirect("seller_dashboard")
        else:
            print(form.errors)
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
