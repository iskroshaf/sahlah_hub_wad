from django.shortcuts import get_object_or_404, redirect, render

from _product_app.forms import ProductCategoryForm, ProductForm
from _product_app.models import Product, ProductCategory
from _shop_app.models import Shop


def product_category_management_view(request, pk):
    title = "Product Category"
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
        "shop": shop,
        "form": form,
        "product_categories": product_categories,
    }

    return render(request, "_product_app/product_category_management.html", context)


def product_register_view(request, pk):
    title = "Product Register"
    shop = get_object_or_404(Shop, shop_id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]
            product_price = form.cleaned_data["product_price"]
            product_description = form.cleaned_data["product_description"]
            product_category_name = form.cleaned_data["product_category_name"]
            product = Product(
                shop=shop,
                product_name=product_name,
                product_price=product_price,
                product_description=product_description,
                product_category_name=product_category_name,
            )
            product.save()
            product.auto_translate(fields=["product_name", "product_description"])
            print("Product registration successfully.")
            return redirect("product_list", pk=shop.shop_id)
        else:
            print("Product registration failed.", form.errors)
    else:
        form = ProductForm()
    context = {"title": title, "shop": shop, "form": form}
    return render(request, "_product_app/product_register.html", context)


def product_list_view(request, pk):
    title = "Product"
    shop = get_object_or_404(Shop, shop_id=pk)
    products = Product.objects.all()
    context = {"title": title, "shop": shop, "products": products}
    return render(request, "_product_app/product_list.html", context)


def product_management_view(request, pk):
    title = "Product Management"
    shop = get_object_or_404(Shop, shop_id=pk)
    context = {"title": title, "shop": shop}
    return render(request, "_product_app/product_management.html", context)
