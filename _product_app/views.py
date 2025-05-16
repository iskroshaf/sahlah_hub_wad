from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language
from django.contrib import messages
from django.contrib.messages import get_messages

from _product_app.forms import ProductCategoryForm, ProductForm
from _product_app.models import Product, ProductCategory,ProductImage
from _shop_app.models import Shop
import logging
import os
import csv
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

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


def product_category_management_view(request):
    title = "Product Category"
    theme = "admin_seller_theme"
    product_categories = ProductCategory.objects.all()

    if request.method == "POST":
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            product_category_name = form.cleaned_data["product_category_name"]
            product_category = ProductCategory(
                product_category_name=product_category_name
            )
            product_category.save()
            product_category.auto_translate(fields=["product_category_name"])
            return redirect("product_category_management")
    else:
        form = ProductCategoryForm()
    context = {
        "title": title,
        "theme": theme,
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


# def product_register_view(request, pk):
#     title = "Product Register"
#     theme = "admin_seller_theme"
#     shop = get_object_or_404(Shop, shop_id=pk)
#     image_errors = None

#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         product_images = request.FILES.getlist("product_images")

#         if not product_images:
#             image_errors = "Please upload at least 1 image."
#         elif len(product_images) > 5:
#             image_errors = "You can upload a maximum of 5 images."

#         if form.is_valid() and not image_errors:
#             product = form.save(commit=False)
#             product.shop = shop
#             current_language = get_language()
#             product.set_current_language(current_language)
#             product.product_name = form.cleaned_data["product_name"]
#             product.product_description = form.cleaned_data["product_description"]

#             # Halal status implementation
#             text = f"{product.product_name} {product.product_description}".lower()

#             try:
#                 response = requests.post(FASTAPI_URL, json={"text": text}, timeout=5)
#                 response.raise_for_status()
#                 ai_prediction = response.json().get("halal_status", "Unknown")
#             except Exception as e:
#                 print(f"AI prediction error: {e}")
#                 ai_prediction = "Unknown"

#             # Keyword detection
#             is_haram = any(word in text for words in haram_keywords.values() for word in words)
#             is_halal = any(word in text for words in halal_keywords.values() for word in words)
#             is_mashbooh = any(word in text for words in mashbooh_keywords.values() for word in words)
#             contains_negation = any(neg in text for neg in NEGATION_WORDS)

#             # Debug log (optional)
#             print(f"AI prediction: {ai_prediction}")
#             print(f"Keywords - Halal: {is_halal}, Haram: {is_haram}, Mashbooh: {is_mashbooh}, Negation: {contains_negation}")

#             # Halal status logic
#             if is_haram and not contains_negation:
#                 product.halal_status = "Haram"
#             elif is_halal and not contains_negation:
#                 product.halal_status = "Halal"
#             elif is_haram and contains_negation:
#                 product.halal_status = "Halal"
#             elif is_halal and contains_negation:
#                 product.halal_status = "Haram"
#             elif is_mashbooh:
#                 product.halal_status = "Mashbooh"
#             elif "tidak diketahui" in text or "meragukan" in text:
#                 product.halal_status = "Mashbooh"
#             elif ai_prediction in ["Halal", "Haram"]:
#                 product.halal_status = ai_prediction
#             else:
#                 product.halal_status = "Mashbooh"

#             product.save()
#             product.auto_translate(fields=["product_name"])
#             product.auto_translate(fields=["product_description"])

#             for file in product_images:
#                 ProductImage.objects.create(product=product, image=file)

#             messages.success(request, "✅ Product registered successfully.")
#             return redirect("product_list", pk=shop.shop_id)
#         else:
            
#             messages.error(request, "❌ Product registration failed.")
#     else:
#         form = ProductForm()

#     context = {
#         "title": title,
#         "theme": theme,
#         "shop": shop,
#         "form": form,
#         "image_errors": image_errors, 
#     }
#     return render(request, "_product_app/product_register.html", context)


def product_register_view(request, pk):
    title = "Product Register"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)
    image_errors = None

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        product_images = request.FILES.getlist("product_images")

        # Validasi image
        if not product_images:
            image_errors = "Please upload at least 1 image."
        elif len(product_images) > 5:
            image_errors = "You can upload a maximum of 5 images."

        if form.is_valid() and not image_errors:
            try:
                product = form.save(commit=False)
                product.shop = shop

                # Multilingual support
                current_language = get_language()
                product.set_current_language(current_language)
                product.product_name = form.cleaned_data["product_name"]
                product.product_description = form.cleaned_data["product_description"]

                # AI Halal status prediction
                text = f"{product.product_name} {product.product_description}".lower()

                try:
                    response = requests.post(FASTAPI_URL, json={"text": text}, timeout=5)
                    response.raise_for_status()
                    ai_prediction = response.json().get("halal_status", "Unknown")
                except Exception as e:
                    logger.warning(f"AI prediction error: {e}")
                    ai_prediction = "Unknown"

                is_haram = any(word in text for words in haram_keywords.values() for word in words)
                is_halal = any(word in text for words in halal_keywords.values() for word in words)
                is_mashbooh = any(word in text for words in mashbooh_keywords.values() for word in words)
                contains_negation = any(neg in text for neg in NEGATION_WORDS)

                # Determine halal_status
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

                for file in product_images:
                    ProductImage.objects.create(product=product, image=file)

                storage = messages.get_messages(request)
                storage.used = True 

                messages.success(request, "✅ Product registered successfully.")
                logger.info("Product registration successful for %s", product.product_name)
                return redirect("product_list", pk=shop.shop_id)

            except Exception as e:
                logger.exception("Unexpected error during product registration")
                messages.error(request, "❌ Unexpected error during product registration.")
        else:
            if image_errors:
                messages.error(request, image_errors)
            else:
                messages.error(request, "❌ Product registration failed. Please check the form.")
            logger.error("Form errors: %s", form.errors)
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
    products = Product.objects.filter(shop=shop)
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


def product_detail_view(request, pk, product_id):
    # pk datang dari prefix di shop_app.urls (shop_id)
    shop = get_object_or_404(Shop, shop_id=pk)
    product = get_object_or_404(Product, product_id=product_id, shop=shop)

    lang = get_language()
    product.set_current_language(lang)

    title = "Product Management"
    theme = "admin_seller_theme"

    existing_count = product.images.count()
    remaining_slots = max(0, 5 - existing_count)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        new_images = request.FILES.getlist("product_images")
        if form.is_valid():
            form.save()
            for img in new_images:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, "✅ Produk dikemaskini.")
            return redirect("product_detail", pk=shop.shop_id, product_id=product.product_id)
        else:
            messages.error(request, "Sila betulkan ralat dalam form.")
    else:
        form = ProductForm(instance=product)

    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "product": product,
        "form": form, 
        "remaining_slots": remaining_slots,
    }
    return render(request, "_product_app/seller_product_detail.html", context)

def product_image_delete_view(request, pk, product_id, image_id):
    shop = get_object_or_404(Shop, shop_id=pk, seller=request.user.seller)
    product = get_object_or_404(Product, product_id=product_id, shop=shop)
    img = get_object_or_404(ProductImage, id=image_id, product=product)

    # Padam fail sebenar (jika perlu)
    img.image.delete(save=False)
    img.delete()
    messages.success(request, "✅ Gambar telah dipadam.")
    return redirect(
        'product_detail', 
        pk=shop.shop_id, 
        product_id=product.product_id
    )