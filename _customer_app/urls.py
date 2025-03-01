from _customer_app import views
from django.urls import path

urlpatterns = [
    path('register/', views.customer_register_view, name='customer_register'),
    path('home/', views.customer_home_view, name='customer_home'),
]