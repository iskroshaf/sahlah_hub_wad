from django.urls import path
from _product_app import views

urlpatterns = [
    path('products/', views.product_list_view, name='product_list'),
    path('product/register/', views.product_register_view, name='product_register'),
    path('product_categories/', views.product_category_management_view, name='product_category_management')
]