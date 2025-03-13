from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language

from _product_app.forms import ProductCategoryForm, ProductForm
from _product_app.models import Product, ProductCategory
from _shop_app.models import Shop


def product_category_management_view(request, pk):
    title = "Product Category"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)
    product_categories = ProductCategory.objects.filter(shop=shop)

    if request.method == "POST":
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            product_category_name = form.cleaned_data["product_category_name"]
            product_category = ProductCategory(
                product_category_name=product_category_name, shop=shop
            )
            product_category.save()
            product_category.auto_translate(fields=["product_category_name"])

            return redirect("product_category_management", pk=shop.shop_id)
    else:
        form = ProductCategoryForm()
    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "form": form,
        "product_categories": product_categories,
    }

    return render(request, "_product_app/product_category_management.html", context)


def product_register_view(request, pk):
    title = "Product Register"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop

            current_language = get_language()
            product.set_current_language(current_language)
            product.product_name = form.cleaned_data["product_name"]
            product.product_description = form.cleaned_data["product_description"]

            product.save()
            product.auto_translate(fields=["product_name", "product_description"])
            print("Product registration successfully.")
            return redirect("product_list", pk=shop.shop_id)
        else:
            print("Product registration failed.", form.errors)
    else:
        form = ProductForm()

    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "form": form,
    }
    return render(request, "_product_app/product_register.html", context)



def product_list_view(request, pk):
    title = "Product"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)
    products = Product.objects.all()
    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "products": products,
    }
    return render(request, "_product_app/product_list.html", context)


def product_management_view(request, pk):
    title = "Product Management"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)
    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
    }
    return render(request, "_product_app/product_management.html", context)
