from _customer_app import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/', views.customer_register_view, name='customer_register'),
    path('home/', views.customer_home_view, name='customer_home'),
    path('update/',views.customer_update_profile,name="Update_profile"),
    path('update/password/', views.customer_update_password, name='customer_update_password'),
    path('update/address/', views.customer_update_address, name='customer_update_address'),
    path('addresses/edit/<int:address_id>/', views.edit_shipping_address, name='customer_edit_address'),
    path("addresses/delete/<int:pk>/", views.delete_shipping_address, name="customer_delete_address"),
    path("product/<str:product_id>/", views.customer_product_detail,name="customer_product_detail"),
    path('orders/', views.customer_order_history, name='order_history'),
    path('orders/<int:order_id>/', views.customer_order_detail, name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)