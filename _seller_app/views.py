from django.shortcuts import redirect, render
from _seller_app.forms import SellerRegisterForm
from _shop_app.models import Shop
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

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
