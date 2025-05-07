from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language

from _product_app.forms import ProductCategoryForm, ProductForm
from _product_app.models import Product, ProductCategory,ProductImage
from _shop_app.models import Shop

import os
import csv
import requests
from django.conf import settings

FASTAPI_URL = "http://127.0.0.1:8001/predict/"

NEGATION_WORDS = [
    # Melayu
    "tidak", "tanpa", "bukan", "bebas dari", "tidak ada", "tidak termasuk", "dikecualikan", "diasingkan",
    "bukan dari", "tiada", "tidak pernah", "tidak wujud", "tidak terkandung", "bukan sebahagian dari",
    "dikeluarkan dari", "bukan bahan utama", "sifar", "tidak dibuat dengan", "tidak mengandungi",
    "tidak diproses dengan", "tidak bersentuhan dengan", "tidak terdapat dalam", "tiada dalam senarai",
    "bukan sebahagian",

    # Inggeris
    "no", "not", "without", "free from", "does not contain", "excluded", "separated from", "absent of",
    "none", "never", "does not exist", "not included", "not part of", "removed from", "zero",
    "not made with", "does not have", "is not processed with", "not in contact with",
    "not found in", "not listed in", "not used in", "not a component of",

    # Arab
    "لا", "ليس", "بدون", "خالي من", "لا يحتوي على", "مستبعد", "معزول", "لا يوجد", "غير موجود",
    "لم يكن", "لم يتم تضمينه", "ليس جزءًا من", "تم إزالته", "صفر", "لم يُصنع بـ", "لا يمتلك",
    "لا يُعالج بـ", "لم يكن ملامسًا", "غير مدرج في القائمة", "لم يُستخدم", "ليس عنصرًا من"
]


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

#Halal Implementation
def load_keywords(file_name):
    file_path = os.path.join(settings.BASE_DIR, '_product_app', 'halal_api', 'data', file_name)
    keywords = {}

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            lang, word = row
            if lang in keywords:
                keywords[lang].append(word.lower())
            else:
                keywords[lang] = [word.lower()]
    return keywords

haram_keywords = load_keywords('haram_keywords.csv')
halal_keywords = load_keywords('halal_keywords.csv')
mashbooh_keywords = load_keywords('mashbooh_keywords.csv')
#Halal Implementation


def product_register_view(request, pk):
    title = "Product Register"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)

    if request.method == "POST":

        form = ProductForm(request.POST, request.FILES)
        files= request.FILES.getlist("product_images")

        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop

            current_language = get_language()
            product.set_current_language(current_language)
            product.product_name = form.cleaned_data["product_name"]
            product.product_description = form.cleaned_data["product_description"]

            # Halal status implementation
            text = f"{product.product_name} {product.product_description}".lower()

            try:
                response = requests.post(FASTAPI_URL, json={"text": text}, timeout=5)
                response.raise_for_status()
                ai_prediction = response.json().get("halal_status", "Unknown")
            except Exception as e:
                print(f"AI prediction error: {e}")
                ai_prediction = "Unknown"

            # Keyword detection
            is_haram = any(word in text for words in haram_keywords.values() for word in words)
            is_halal = any(word in text for words in halal_keywords.values() for word in words)
            is_mashbooh = any(word in text for words in mashbooh_keywords.values() for word in words)
            contains_negation = any(neg in text for neg in NEGATION_WORDS)

            # Debug log (optional)
            print(f"AI prediction: {ai_prediction}")
            print(f"Keywords - Halal: {is_halal}, Haram: {is_haram}, Mashbooh: {is_mashbooh}, Negation: {contains_negation}")

            # Halal status logic
            if is_haram and not contains_negation:
                product.halal_status = "Haram"
            elif is_halal and not contains_negation:
                product.halal_status = "Halal"
            elif is_haram and contains_negation:
                product.halal_status = "Halal"
            elif is_halal and contains_negation:
                product.halal_status = "Haram"
            elif is_mashbooh:
                product.halal_status = "Mashbooh"
            elif "tidak diketahui" in text or "meragukan" in text:
                product.halal_status = "Mashbooh"
            elif ai_prediction in ["Halal", "Haram"]:
                product.halal_status = ai_prediction
            else:
                product.halal_status = "Mashbooh"

            product.save()
            product.auto_translate(fields=["product_name"])
            product.auto_translate(fields=["product_description"])

            for file in files:
                ProductImage.objects.create(product=product, image=file)

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
