from django.urls import path, include

from _shop_app import views

urlpatterns = [
     path('', views.shop_list_view, name='shop_list'),
     path('register/', views.shop_register_view, name='shop_register'),
     path('<str:pk>/dashboard/', views.shop_dashboard_view, name='shop_dashboard'),
     path('<str:pk>/products/', include('_product_app.urls')),
]

