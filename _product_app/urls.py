from django.urls import path
from _product_app import views

urlpatterns = [
    path('', views.product_list_view, name='product_list')
]