from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language
from django.contrib import messages
from django.contrib.messages import get_messages
from decimal import Decimal
from _product_app.forms import ProductCategoryForm, ProductForm,VariantFormSet
from _product_app.models import Product, ProductCategory,ProductImage,ProductVariant
from django.db.models import Case, When, Value, IntegerField, Q,Min,Sum
from _shop_app.models import Shop
import logging
import os
import csv
import requests
from django.conf import settings

import builtins 


from pprint import pprint
import json  

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
    PREFIX = "variants"

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        variant_fs  = VariantFormSet(request.POST, prefix=PREFIX)
        product_images = request.FILES.getlist("product_images")

        
        if not product_images:
            image_errors = "Please upload at least 1 image."
        elif len(product_images) > 5:
            image_errors = "You can upload a maximum of 5 images."


        if form.is_valid() and (form.cleaned_data["no_variant"] or variant_fs.is_valid()) and not image_errors:
            try:
                product = form.save(commit=False)
                product.shop = shop

                Category: ProductCategory = form.cleaned_data['product_category_name']
                cat_name = Category.product_category_name.strip().lower()

                product.no_variant = form.cleaned_data["no_variant"]
               
                current_language = get_language()
                product.set_current_language(current_language)
                product.product_name = form.cleaned_data["product_name"]
                product.product_description = form.cleaned_data["product_description"]

                
                if cat_name in ["food", "drink"]:
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
                else:
                    product.halal_status = "None"


                if not form.cleaned_data["no_variant"]:
                # Cari harga paling rendah yang TIDAK ditanda DELETE
                    prices = [
                        v["variant_price"]
                        for v in variant_fs.cleaned_data
                        if not v.get("DELETE", False) and v.get("variant_price") is not None
                    ]
                    # Jika at least satu baris, ambil min; jika tiada, guna 0
                    product.product_price = min(prices) if prices else Decimal("0.00")
                else:
                    product.product_price = Decimal("0.00")
                    
                product.save()
                product.auto_translate(fields=["product_name"])
                product.auto_translate(fields=["product_description"])


               
                if form.cleaned_data["no_variant"]:
                    ProductVariant.objects.create(
                        product          = product,
                        variant_name     = "Default",
                        variant_price    = form.cleaned_data["product_price"],
                        variant_quantity = form.cleaned_data["base_quantity"] or 0,
                        is_active        = True
                    )
                    product.product_price = form.cleaned_data["product_price"]
                    product.save(update_fields=["product_price"])
                else:
                    variant_fs.instance = product
                    variant_fs.save()
                    cheapest = product.variants.filter(is_active=True).aggregate(Min("variant_price"))["variant_price__min"]
                    if cheapest is not None:
                        product.product_price = cheapest
                        product.save(update_fields=['product_price'])

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

            if form.errors:
                print("\n======= ProductForm errors =======")
                print(json.dumps(form.errors.get_json_data(), indent=2))

            if 'variant_fs' in locals():          
                 if variant_fs.non_form_errors():
                    print("\n=== VariantFormSet NON-FIELD errors ===")
                    pprint(variant_fs.non_form_errors().as_data())

            for idx, err_dict in enumerate(variant_fs.errors):
                if err_dict:
                    print(f"\n--- Variant row {idx} errors ---")
                    pprint(err_dict)
    else:
        form = ProductForm()
        variant_fs = VariantFormSet(prefix=PREFIX)

    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "form": form,
        "image_errors": image_errors, 
        "variant_fs": variant_fs,

    }
    return render(request, "_product_app/product_register.html", context)


def product_list_view(request, pk):
    title = "Product"
    theme = "admin_seller_theme"
    shop = get_object_or_404(Shop, shop_id=pk)

    # ── GET parameters ─────────────────────────────────────
    q      = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    sort   = request.GET.get('sort', '').strip()

    ALL_STATUSES = ['None', 'Halal', 'Haram', 'Mashbooh']
    VALID_STATUSES = set(ALL_STATUSES)

    # ── Base queryset (Parler active language) ─────────────
    qs = Product.objects.active_translations(request.LANGUAGE_CODE).filter(shop=shop)

    # ── Search product name (current language) ─────────────
    if q:
        qs = qs.filter(translations__product_name__icontains=q)

    # ── Status priority (bawa status terpilih ke atas) ─────
    if status in VALID_STATUSES:
        idx     = ALL_STATUSES.index(status)
        rotated = ALL_STATUSES[idx:] + ALL_STATUSES[:idx]   # putar list
        whens   = [When(halal_status=s, then=Value(pos)) for pos, s in enumerate(rotated)]
        qs = qs.annotate(
            dyn_rank=Case(*whens, default=Value(len(ALL_STATUSES)), output_field=IntegerField())
        )
    # Jika tiada status dipilih, dyn_rank tiada (abaikan)

    # ── Sorting order list ─────────────────────────────────
    ordering = []
    if status in VALID_STATUSES:
        ordering.append('dyn_rank')              # status terpilih di atas
    if sort == 'price_desc':
        ordering.append('-product_price')
    elif sort == 'price_asc':
        ordering.append('product_price')
    ordering.append('translations__product_name')  # fallback
    qs = qs.order_by(*ordering)

    return render(request, "_product_app/product_list.html", {
        "title": title,
        "theme": theme,
        "shop": shop,
        "products": qs,
        "q": q,
        "current_status": status,
        "current_sort": sort,
    })

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
    shop = get_object_or_404(Shop, shop_id=pk)
    product = get_object_or_404(Product, product_id=product_id, shop=shop)

    # Set bahasa semasa
    lang = get_language()
    product.set_current_language(lang)

    title = "Product Management"
    theme = "admin_seller_theme"

    # Kirakan baki slot gambar (maks 5)
    existing_count = product.images.count()
    remaining_slots = max(0, 5 - existing_count)

    # Simpan state asal no_variant
    prev_no_variant = product.no_variant

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        # Papar hanya varian yang aktif
        active_variants_qs = product.variants.filter(is_active=True)
        variant_fs = VariantFormSet(
            request.POST,
            prefix="variants",
            instance=product,
            queryset=active_variants_qs
        )

        new_images = request.FILES.getlist("product_images")

        no_variant_now = form.data.get("no_variant") == "on"
        if no_variant_now:
            active_variants_qs = product.variants.none()
        else:
            active_variants_qs = (
                product.variants.filter(is_active=True)
                                .exclude(variant_name="Default")              
            )
        variant_fs = VariantFormSet(
        request.POST,
        prefix="variants",
        instance=product,
        queryset=active_variants_qs,
        )
        # Validasi: jangan melebihi baki slot gambar
        if len(new_images) > remaining_slots:
            messages.error(request, f"Maksimum tinggal {remaining_slots} slot imej sahaja.")
        elif form.is_valid() and (no_variant_now or variant_fs.is_valid()):
            try:
                # Simpan perubahan Product tanpa commit dulu
                product = form.save(commit=False)
                product.set_current_language(lang)
                product.product_name = form.cleaned_data["product_name"]
                product.product_description = form.cleaned_data["product_description"]

                # --------- Logik HALAL STATUS ----------
                kategori_obj = form.cleaned_data["product_category_name"]
                cat_name = kategori_obj.product_category_name.strip().lower()
                if cat_name in ["food", "drink"]:
                    text = f"{product.product_name} {product.product_description}".lower()
                    try:
                        resp = requests.post(FASTAPI_URL, json={"text": text}, timeout=5)
                        resp.raise_for_status()
                        ai_pred = resp.json().get("halal_status", "Unknown")
                    except Exception as e:
                        logger.warning(f"AI prediction error: {e}")
                        ai_pred = "Unknown"

                    is_haram    = any(w in text for vals in haram_keywords.values()   for w in vals)
                    is_halal    = any(w in text for vals in halal_keywords.values()   for w in vals)
                    is_mashbooh = any(w in text for vals in mashbooh_keywords.values() for w in vals)
                    ada_negasi  = any(neg in text for neg in NEGATION_WORDS)

                    if is_haram and not ada_negasi:
                        product.halal_status = "Haram"
                    elif is_halal and not ada_negasi:
                        product.halal_status = "Halal"
                    elif is_haram and ada_negasi:
                        product.halal_status = "Halal"
                    elif is_halal and ada_negasi:
                        product.halal_status = "Haram"
                    elif is_mashbooh or "tidak diketahui" in text or "meragukan" in text:
                        product.halal_status = "Mashbooh"
                    elif ai_pred in ["Halal", "Haram"]:
                        product.halal_status = ai_pred
                    else:
                        product.halal_status = "Mashbooh"
                else:
                    product.halal_status = "None"
                # ----------------------------------------

                # --------- LOGIK VARIANT ↔ NO_VARIANT ---------------
                if prev_no_variant and not no_variant_now:
                    # [A]  TIADA → ADA varian
                    # 1) Non-aktifkan baris “Default” lama
                    product.variants.filter(variant_name="Default").update(is_active=False)

                    # 2) Simpan semua varian baru dari FormSet (is_active=True)
                    variant_fs.instance = product
                    variant_fs.save()

                    # 3) Kemas kini harga produk = harga termurah varian aktif
                    # cheapest = product.variants.filter(is_active=True).aggregate(
                    #     Min("variant_price")
                    # )["variant_price__min"]
                    # product.product_price = cheapest or Decimal("0.00")

                    # 4) Dalam mod varian, stok (product_quantity) set ke 0
                    # product.product_quantity = 

                    product.product_price = (
                        product.variants.filter(is_active=True)
                                        .aggregate(Min("variant_price"))["variant_price__min"]
                        or Decimal("0.00")
                        )
                    
                    product.product_quantity = ( product.variants.filter(is_active=True).aggregate(Sum("variant_quantity"))["variant_quantity__sum"] or 0)



                elif not prev_no_variant and no_variant_now:
                    # [B]  ADA → TIADA varian
                    # 1) Non-aktifkan semua varian sedia ada (termasuk Default lama & varian lain)
                    product.variants.update(is_active=False)

                    # 2) Cari Default lama; jika wujud, update; jika tak, cipta baru
                    
                    default_var = product.variants.filter(variant_name="Default").first()
                    if default_var:
                        # Update baris sedia ada
                        default_var.is_active        = True
                        default_var.variant_price    = form.cleaned_data["product_price"]
                        default_var.variant_quantity = form.cleaned_data.get("base_quantity") or 0
                        default_var.save(update_fields=["is_active", "variant_price", "variant_quantity"])
                    else:
                        # Cipatahnc Default baru jika tiada
                        default_var = ProductVariant.objects.create(
                            product          = product,
                            variant_name     = "Default",
                            variant_price    = form.cleaned_data["product_price"],
                            variant_quantity = form.cleaned_data.get("base_quantity") or 0,
                            is_active        = True
                        )

                    # 3) Kemas kini harga & stok produk
                    product.product_price    = default_var.variant_price
                    product.product_quantity = default_var.variant_quantity

                else:
                    # [C]  Mode tidak berubah
                    if no_variant_now:
                        # Masih TIADA varian → update harga & stok tunggal
                        product.product_price    = form.cleaned_data["product_price"]
                        product.product_quantity = form.cleaned_data.get("base_quantity") or 0
                        (
                            product.variants
                            .filter(variant_name="Default")
                            .update(
                                variant_price    = product.product_price,
                                variant_quantity = product.product_quantity,
                                is_active        = True,   # pastikan hidup
                            )
                        )
                    else:
                        # Masih ADA varian → simpan FormSet biasa
                        variant_fs.instance = product
                        variant_fs.save()
                        # cheapest = product.variants.filter(is_active=True).aggregate(
                        #     Min("variant_price")
                        # )["variant_price__min"]
                        # product.product_price = cheapest or Decimal("0.00")
                        # product.product_quantity = 0
                        product.product_price = (
                                product.variants.filter(is_active=True)
                                                .aggregate(Min("variant_price"))["variant_price__min"]
                                or Decimal("0.00")
                            )
                        product.product_quantity = (
                                product.variants.filter(is_active=True)
                                                .aggregate(Sum("variant_quantity"))["variant_quantity__sum"]
                                or 0
                            )

                # Simpan flag no_variant dan commit Product
                product.no_variant = no_variant_now
                product.save()
                # ------------------------------------------------------

                # Auto-translate fields
                product.auto_translate(fields=["product_name"])
                product.auto_translate(fields=["product_description"])

                # Simpan gambar baru
                for img in new_images:
                    ProductImage.objects.create(product=product, image=img)

                # Clear old messages
                storage = messages.get_messages(request)
                storage.used = True

                messages.success(request, "✅ Product updated.")
                logger.info("Product updated: %s", product.product_name)
                return redirect("product_detail", pk=shop.shop_id, product_id=product.product_id)

            except Exception as e:
                logger.exception("Error semasa update product")
                messages.error(request, "❌ Unexpected error semasa update product.")
        else:
            # Validasi gagal
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, "❌ Sila betulkan kesilapan dalam borang.")
            logger.error("Update failed, form errors: %s", form.errors)
            if variant_fs.errors:
                for idx, err in enumerate(variant_fs.errors):
                    if err:
                        print(f"--- Variant row {idx} errors ---")
                        print(err)

    else:
        # (GET) Init form & formset
        form = ProductForm(instance=product)
        active_variants_qs = product.variants.filter(is_active=True).exclude(variant_name="Default")
        variant_fs = VariantFormSet(
            prefix   = "variants",
            instance = product,
            queryset = active_variants_qs
        )
   

    active_variants = (
    product.variants.filter(is_active=True)
                    .exclude(variant_name="Default")
    )

    global_qty = (
        active_variants.aggregate(Sum("variant_quantity"))["variant_quantity__sum"]
        or 0
    )

    context = {
        "title": title,
        "theme": theme,
        "shop": shop,
        "product": product,
        "form": form,
        "variant_fs": variant_fs,
        "variant_list": active_variants,
        "global_qty":  active_variants.aggregate(     # ← baharu
                      Sum("variant_quantity")
                   )["variant_quantity__sum"] or 0,
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