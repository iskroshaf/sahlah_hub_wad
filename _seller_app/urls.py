from django.urls import path

from _seller_app import views

urlpatterns = [
    path('register/', views.seller_register_view, name='seller_register'),
    path('dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
]