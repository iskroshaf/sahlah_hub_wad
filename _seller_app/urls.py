from django.urls import path

from _seller_app import views
from _shop_app.views import shop_list_view, shop_register_view

urlpatterns = [
    path('register/', views.seller_register_view, name='seller_register'),
    path('dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    
    path('shop/register/', shop_register_view, name='shop_register'),
    path('shops/', shop_list_view, name='shop_list'),
]