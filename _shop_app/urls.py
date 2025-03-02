from django.urls import path, include

from _shop_app import views

urlpatterns = [
    path('shops/', views.shop_list_view, name='shop_list'),
    path('shop/register/', views.shop_register_view, name='shop_register'),
    path('shop/<str:pk>/', include([
        path('dashboard/', views.shop_dashboard_view, name='shop_dashboard'),
        path('', include('_product_app.urls')),  
    ])),
]


