from django.urls import path

from _seller_app import views as seller_views
from _shop_app.views import shop_list_view, shop_register_view,seller_edit_shop

# urlpatterns = [
#     path('register/', views.seller_register_view, name='seller_register'),
#     path('dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    
#     path('shop/register/', shop_register_view, name='shop_register'),
#     path('shops/', shop_list_view, name='shop_list'),
# ]

urlpatterns = [
    path('register/',seller_views.seller_register_view, name='seller_register'),
    path('dashboard/',seller_views.seller_dashboard_view, name='seller_dashboard'),

    path('shop/register/',shop_register_view, name='shop_register'),
    path('shops/',shop_list_view, name='shop_list'),

    # ← Edit route:
    path(
        'shops/<str:shop_id>/edit/',
        seller_edit_shop,
        name='seller_edit_shop'
    ),
]