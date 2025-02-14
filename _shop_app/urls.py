from django.urls import path

from _shop_app import views

urlpatterns = [
     path('register/', views.shop_register_view, name='shop_register'),
]

