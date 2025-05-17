from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
# from _shop_app.models import ProductCategory
from _shop_app.models import Shop
from django.views import View
from _seller_app.models import Seller
from django.contrib import messages

def admin_dashboard_view(request):
    title = "Admin Dashboard"
    theme = "admin_seller_theme"
    user = request.user
    context = {
        "title": title,
        "theme": theme,
        "user": user,
    }
    return render(request, "_admin_app/admin_dashboard.html", context)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff



# Senarai Kedai Belum Diluluskan
class ShopApprovalListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Shop
    template_name = "_admin_app/shop_approval_list.html"
    context_object_name = "pending_shops"
    def get_queryset(self):
        return Shop.objects.filter(is_approved=False)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Kelulusan Kedai"
        ctx['theme'] = "admin_seller_theme"
        return ctx


class ProductCategoryManageView(LoginRequiredMixin, AdminRequiredMixin, View):

    template_name = "_admin_app/product_category_management.html"

    def get(self, request):
        form = ProductCategoryForm()
        categories = ProductCategory.objects.all().order_by('id')
        context = {
            "title": "Product Categories",
            "theme": "admin_seller_theme",
            "form": form,
            "product_categories": categories
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategori baru telah berjaya didaftarkan.")
            return redirect(reverse('admin_category_product_list'))
        categories = ProductCategory.objects.all().order_by('id')
        context = {
            "title": "Product Categories",
            "theme": "admin_seller_theme",
            "form": form,
            "product_categories": categories
        }
        return render(request, self.template_name, context)


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

    return render(request, "_admin_app/seller_approval_list.html", {
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
        seller.status      = 'A'      # Update field `status` di CustomUser
        msg = "diluluskan"
    elif action == "reject":
        seller.is_approved = False
        seller.status      = 'I'      # 'I' = Inactive, akan paparkan badge Rejected
        msg = "ditolak"
    elif action == "revoke":
        # jika ada butang revoke, kembalikan ke Pending
        seller.is_approved = False
        seller.status      = 'P'
        msg = "pembatalan kelulusan"
    else:
        messages.error(request, "Tindakan tidak dikenali.")
        return redirect("seller_approval_list")

    # Simpan kedua-dua ruangan dalam satu operasi
    seller.save(update_fields=["is_approved", "status"])
    messages.success(request, f"Peniaga {seller.username} telah {msg}.")

    return redirect("seller_approval_list")