from django.urls import path,reverse_lazy

from _seller_app import views as seller_views
from .views import SellerPasswordChangeView, SellerPasswordChangeDoneView
from _shop_app.views import shop_list_view, shop_register_view,seller_edit_shop
from django.contrib.auth import views as auth_views

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

   
    path(
        'shops/<str:shop_id>/edit/',seller_edit_shop,name='seller_edit_shop'
    ),

# password modified
    path( 'password/change/', SellerPasswordChangeView.as_view(),name='seller_password_change'
    ),
    path('password/change/done/',SellerPasswordChangeDoneView.as_view(),name='seller_password_change_done'
    ),
]