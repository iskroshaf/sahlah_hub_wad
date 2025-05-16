from django.urls import path, include
from _admin_app import views
from .views import admin_dashboard_view

urlpatterns = [
    path('dashboard/',views.admin_dashboard_view, name='admin_dashboard'),
    path('products/', include('_product_app.urls')),
]