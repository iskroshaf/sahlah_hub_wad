from django.shortcuts import redirect, render
from _seller_app.forms import SellerRegisterForm
from _shop_app.models import Shop


def seller_register_view(request):
    title = "Seller Register"
    theme = "customer_theme"
    if request.method == "POST":
        form = SellerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = "A"
            user.role = "S"
            user.save()
            print("Register Successful")
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = SellerRegisterForm()
    context = {"title": title, "theme": theme, "form": form}
    return render(request, "_seller_app/seller_register.html", context)


def seller_dashboard_view(request):
    title = "Seller Dashboard"
    theme = "admin_seller_theme"
    user = request.user
    shops = Shop.objects.filter(seller=user)
    context = {
        "title": title,
        "theme": theme,
        "user": user,
        "shops": shops,
    }
    return render(request, "_seller_app/seller_dashboard.html", context)
