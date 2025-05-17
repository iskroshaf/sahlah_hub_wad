from django.shortcuts import redirect, render,get_object_or_404, redirect
from _seller_app.forms import SellerRegisterForm,SellerProfileForm
from _shop_app.models import Shop
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib import messages
from _seller_app.models import Seller

def seller_register_view(request):
    title = "Seller Register"
    theme = "customer_theme"
    if request.method == "POST":
        form = SellerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = "P"
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

class SellerPasswordChangeView(PasswordChangeView):
    template_name = '_seller_app/seller_changePassword.html'
    success_url = reverse_lazy('seller_password_change_done')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['theme'] = 'admin_seller_theme'
        ctx['title'] = 'Tukar Kata Laluan'
        return ctx

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
       
        for fname in ('old_password', 'new_password1', 'new_password2'):
            form.fields[fname].widget.attrs.update({
                'class': 'form-control'
            })
        return form

class SellerPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = '_seller_app/seller_changePasswordDone.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['theme'] = 'admin_seller_theme'
        ctx['title'] = 'Katalaluan Dikemaskini'
        return ctx


def seller_profile_update_view(request):
    seller = request.user.seller
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('seller_profile_update')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SellerProfileForm(instance=seller)

    return render(request, '_seller_app/seller_update_profile.html', {
        'form': form,
        'title': 'Update Profile',
        'theme': 'admin_seller_theme',
    })

def seller_profile_view(request):
    
    title = "Seller Profile"
    theme = "admin_seller_theme"
    context = {
        "theme": theme,
        "title":title,
        
    }
    return render(request, "_seller_app/seller_profile.html", context)



def seller_approval_list_view(request):
    tab = request.GET.get("status", "pending")
    if tab == "pending":
        qs = Seller.objects.filter(status='P')
    elif tab == "approved":
        qs = Seller.objects.filter(status='A')
    elif tab == "rejected":
        qs = Seller.objects.filter(status='I')
    else:  # all
        qs = Seller.objects.all()

    counts = {
        "pending":  Seller.objects.filter(status='P').count(),
        "approved": Seller.objects.filter(status='A').count(),
        "rejected": Seller.objects.filter(status='I').count(),
        "all":      Seller.objects.count(),
    }
    status_tabs = [
        ("pending",  f"Pending ({counts['pending']})"),
        ("approved", f"Approved ({counts['approved']})"),
        ("rejected", f"Rejected ({counts['rejected']})"),
        ("all",      f"All ({counts['all']})"),
    ]

    return render(request, "_seller_app/seller_approval.html", {
        "title":          "Seller Approval",
        "theme":          "admin_seller_theme",
        "sellers":        qs.order_by("-date_joined"),
        "current_status": tab,
        "status_tabs":    status_tabs,
    })


def seller_approval_toggle_view(request, seller_id, action):
    if request.method != "POST":
        return redirect("seller_approval_list")

    seller = get_object_or_404(Seller, seller_id=seller_id)

    if action == "approve":
        seller.is_approved = True
        seller.status      = 'A'      
        msg = "diluluskan"
    elif action == "reject":
        seller.is_approved = False
        seller.status      = 'I'      
        msg = "ditolak"
    elif action == "revoke":
       
        seller.is_approved = False
        seller.status      = 'P'
        msg = "pembatalan kelulusan"
    else:
        messages.error(request, "Tindakan tidak dikenali.")
        return redirect("seller_approval_list")

    seller.save(update_fields=["is_approved", "status"])
    messages.success(request, f"Peniaga {seller.username} telah {msg}.")

    return redirect("seller_approval_list")