from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('',  views.cart_page,         name='view'),
    path('add/', views.add_to_cart_view, name='add'),
    path('ajax/set-qty/<int:variant_id>/', views.ajax_set_qty, name='ajax-set-qty'),
    path('ajax/remove-item/<int:variant_id>/', views.ajax_remove_item, name='ajax-remove-item'),
    path('checkout/', views.checkout, name='checkout'),
]
