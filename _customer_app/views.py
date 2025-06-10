from django.shortcuts import render, redirect, get_object_or_404
from _customer_app.forms import CustomerRegisterForm,ProfileUpdateForm,PasswordChangeForm,ShippingAddressForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash 
from .models import ShippingAddress
from _product_app.models import Product
from django.core.paginator import Paginator
from django.db.models import Sum


def customer_register_view(request):
    title = "Register"
    theme = "customer_theme"
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = "A"
            user.role = "C"
            user.save()
            print("Register Successful")
            messages.success(request, "Create account was succesfully ! Please Log In First ;) ")
            return redirect("login")
        else:
            # print(form.errors)
            if form.errors.get('username'):
                messages.error(request, f"Username error: {form.errors['username'][0]}")
            elif form.errors.get('email'):
                messages.error(request, f"Error with email: {form.errors['email'][0]}")  # Mesej ralat email
            elif form.errors.get('password2'):
                messages.error(request, f"Error with password confirmation: {form.errors['password2'][0]}")  # Mesej ralat password

    else:
        form = CustomerRegisterForm()

    context = {"title": title, "theme": theme, "form": form}
    return render(request, "_customer_app/customer_register.html", context)


def customer_home_view(request):
    title = "Customer Home"
    theme = "customer_theme"
    products_qs = Product.objects.filter(product_availability="available",shop__shop_status=1).order_by('-product_id')  # contoh susun ikut tarikh imbasan
    paginator = Paginator(products_qs, 12)  # 12 produk per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": title,
        "theme": theme,
        "products": page_obj.object_list,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "paginator": paginator,
    }
    return render(request, "_customer_app/customer_home.html", context)



def customer_update_profile(request):
    title = "Update Profile"
    theme = "customer_theme"
    context = {"title": title, "theme": theme}
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # cleaned_data = form.cleaned_data
            # current_password = cleaned_data.get("current_password")
            # new_password = cleaned_data.get("new_password")

            # if current_password and new_password:
            #     if not user.check_password(current_password):
            #         form.add_error('current_password', 'The current password is incorrect.')
            #         context['form'] = form
            #         return render(request, "_customer_app/customer_update_profile.html", context)
            #     user.set_password(new_password)

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("customer_home")
        else:
            context['form'] = form
    else:
        form = ProfileUpdateForm(instance=user)

    context['form'] = form
    return render(request, "_customer_app/customer_update_profile.html", context)



 # pastikan import ini ada


def customer_update_password(request):
    title = "Change Password"
    theme = "customer_theme"
    context = {"title": title, "theme": theme}

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # elak auto logout
            messages.success(request, "Password updated successfully!")
            return redirect("customer_update_password")
        else:
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, "_customer_app/customer_update_password.html", context)

##################################################################### Address Section ###################################################


####################################### Update_Homepagee###########################################
def customer_update_address(request):
    title = "Customer Address"
    theme = "customer_theme"

    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, "Address Add successfully!")
            return redirect('customer_update_address')
    else:
        form = ShippingAddressForm()  # ✅ pastikan ini wujud untuk GET request

    addresses = ShippingAddress.objects.filter(user=request.user)

    context = {
        "title": title,
        "theme": theme,
        "form": form,
        "addresses": addresses,
    }
    return render(request, "_customer_app/customer_address.html", context)
################################## End Update Homepage ###################################################################



################################# Edit Address Customer ########################################################
def edit_shipping_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('customer_update_address') 
    else:
        form = ShippingAddressForm(instance=address)

    context = {
        'form': form,
        'title': 'Edit Shipping Address',
        'theme': 'customer_theme',
        'address': address,
    }
    return render(request, '_customer_app/customer_edit_address.html', context)
################################################ End Edit Address Customer ###################################################################


################################################ Delete Address Customer #############################################
def delete_shipping_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect("Update_profile")  
    
    return render(request, "_customer_app/customer_delete_address.html", {"address": address})
################################################ End Delete Address Customer #############################################

def customer_product_detail(request, product_id):
    # ────────── Ambil produk ──────────
    product = get_object_or_404(
        Product.objects.select_related("shop"),
        product_id=product_id,
        product_availability="available",
        shop__shop_status=1,
    )

    # ────────── Gambar ──────────
    images_main = list(product.images.all())
    if not images_main:
        images_main = [ProductImage(image="images/placeholder.png")]

    # ────────── Variant vs non-variant ──────────
    if product.no_variant:
        variant_list       = []
        global_qty         = product.product_quantity
        checked_variant_id = None                       # 🔹 tiada varian
        selected_variant   = None    
    else:
        variant_list = product.variants.filter(is_active=True)
        global_qty   = (
            variant_list.aggregate(Sum("variant_quantity"))["variant_quantity__sum"]
            or 0
        )

        # 🔹 Cari varian pertama yang masih ada stok (>0)
        checked_variant_id = next(
            (v.id for v in variant_list if v.variant_quantity > 0), 
            None
        )

        selected_variant = next(                       # ➋
            (v for v in variant_list if v.id == checked_variant_id),
            None
        )

    # ────────── Context ──────────
    context = {
        "title":            product.product_name,
        "theme":            "customer_theme",
        "product":          product,
        "variant_list":     variant_list,
        "global_qty":       global_qty,
        "images_main":      images_main,
        "checked_variant_id": checked_variant_id,       # 🔹 hantar ke template
        "selected_variant"   : selected_variant, 
    }
    return render(request, "_customer_app/customer_product_detail.html", context)
