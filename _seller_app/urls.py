from django.urls import path,reverse_lazy

from _seller_app import views as seller_views
from .views import SellerPasswordChangeView, SellerPasswordChangeDoneView,seller_approval_list_view,seller_approval_toggle_view
from _shop_app.views import shop_list_view, shop_register_view,seller_edit_shop
from django.contrib.auth import views as auth_views
from . import views

# urlpatterns = [
#     path('register/', views.seller_register_view, name='seller_register'),
#     path('dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    
#     path('shop/register/', shop_register_view, name='shop_register'),
#     path('shops/', shop_list_view, name='shop_list'),
# ]

urlpatterns = [
    path('register/',seller_views.seller_register_view, name='seller_register'),
    path('dashboard/',seller_views.seller_dashboard_view, name='seller_dashboard'),
   
    path('profile', seller_views.seller_profile_view, name='seller_profile'),
     path('profile/update/', seller_views.seller_profile_update_view,name='seller_profile_update'),

    path('shop/register/',shop_register_view, name='shop_register'),
    path('shops/',shop_list_view, name='shop_list'),
    path(
        'shops/<str:shop_id>/edit/',seller_edit_shop,name='seller_edit_shop'
    ),
    path('seller-approval/', views.seller_approval_list_view, name='seller_approval_list'),
    path('seller-approval/<str:seller_id>/<str:action>/',views.seller_approval_toggle_view, name='seller_approval_toggle'),

    path("orders/",               views.seller_order_list,   name="order_list_seller"),
    path("orders/<int:order_id>/", views.seller_order_detail, name="order_detail_seller"),



# password modified
    path( 'password/change/', SellerPasswordChangeView.as_view(),name='seller_password_change'
    ),
    path('password/change/done/',SellerPasswordChangeDoneView.as_view(),name='seller_password_change_done'
    ),

    
]