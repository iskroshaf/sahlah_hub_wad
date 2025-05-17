from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
# from _shop_app.models import ProductCategory
from _shop_app.models import Shop
from django.views import View
from _seller_app.models import Seller
from django.contrib import messages
from django.db.models import Count, Q

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
        message_text       = f"Seller {seller.username} has been approved."
        level              = messages.SUCCESS

    elif action == "reject":
        seller.is_approved = False
        seller.status      = 'I'
        message_text       = f"Seller {seller.username} has been rejected."
        level              = messages.SUCCESS

    elif action == "revoke":
        seller.is_approved = False
        seller.status      = 'P'
        message_text       = f"Approval for seller {seller.username} has been revoked."
        level              = messages.SUCCESS

    else:
        messages.error(request, "Unrecognized action.")
        return redirect("seller_approval_list")

    seller.save(update_fields=["is_approved", "status"])
    messages.add_message(request, level, message_text)

    return redirect("seller_approval_list")



def shop_approval_list_view(request):
    tab = request.GET.get("status", "pending")
    if tab == "active":
        base_qs = Shop.objects.filter(shop_status='1')
    elif tab == "all":
        base_qs = Shop.objects.all()
    else:
        base_qs = Shop.objects.filter(shop_status='2')

 
    counts = {
        "pending": Shop.objects.filter(shop_status='2').count(),
        "active":  Shop.objects.filter(shop_status='1').count(),
        "all":     Shop.objects.count(),
    }
    status_tabs = [
        ("pending", f"Pending ({counts['pending']})"),
        ("active",  f"Active  ({counts['active']})"),
        ("all",     f"All     ({counts['all']})"),
    ]


    shops = list(
        base_qs
        .select_related('seller')
        .order_by('-pk')
    )

    
    for shop in shops:
        shop.approved_count = Shop.objects.filter(
            seller=shop.seller,
            shop_status='1'
        ).count()

    return render(request, "_shop_app/shop_approval_list.html", {
        "title":          "Shop Approval",
        "theme":          "admin_seller_theme",
        "shops":          shops,
        "current_status": tab,
        "status_tabs":    status_tabs,
    })

def shop_approval_toggle_view(request, shop_id, action):
    if request.method != "POST":
        return redirect("shop_approval_list")

    shop = get_object_or_404(Shop, shop_id=shop_id)

    if action == "approve":
        shop.shop_status = '1'  
        msg = "approve"
    elif action == "reject":
        shop.shop_status = '3'  
        msg = "reject"
    else:
        messages.error(request, "Tindakan tidak dikenali.")
        return redirect("shop_approval_list")

    shop.save(update_fields=["shop_status"])
    messages.success(request, f"Shop “{shop.shop_name}” has  {msg}.")
    return redirect("shop_approval_list")





