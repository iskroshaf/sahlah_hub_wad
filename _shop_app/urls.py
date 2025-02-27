from django.urls import path

from _shop_app import views

urlpatterns = [
     path('register/', views.shop_register_view, name='shop_register'),
     path('list/', views.shop_list_view, name='shop_list'),
     path('dashboard/<str:pk>', views.shop_dashboard_view, name='shop_dashboard'),
]

