from django.urls import path
from _admin_app import views
from .views import admin_dashboard_view

urlpatterns = [
    path('dashboard/',views.admin_dashboard_view, name='admin_dashboard'),
    path('product-categories/', views.ProductCategoryManageView.as_view(),name='admin_category_product_list'),
]