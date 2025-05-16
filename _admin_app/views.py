from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
# from _shop_app.models import ProductCategory
from _shop_app.models import Shop
from django.views import View

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