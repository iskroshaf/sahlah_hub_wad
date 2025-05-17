from django.urls import path, include
from _admin_app import views
from .views import admin_dashboard_view

urlpatterns = [
    path('dashboard/',views.admin_dashboard_view, name='admin_dashboard'),
    path('products/', include('_product_app.urls')),

    path('seller-approval/', views.seller_approval_list_view, name='seller_approval_list'),
    path('seller-approval/<str:seller_id>/<str:action>/',views.seller_approval_toggle_view, name='seller_approval_toggle'),
   
    path('shop-approval/', views.shop_approval_list_view, name='shop_approval_list'),
    path('shop-approval/<str:shop_id>/<str:action>/', views.shop_approval_toggle_view, name='shop_approval_toggle'),
]