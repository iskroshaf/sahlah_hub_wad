from django.urls import path, include

from _shop_app import views

urlpatterns = [
    path('<str:pk>/', include([
        path('dashboard/', views.shop_dashboard_view, name='shop_dashboard'),
        path('', include('_product_app.urls')),  
    ])),
]


