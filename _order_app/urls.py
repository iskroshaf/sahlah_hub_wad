from django.urls import path
from . import views

       

urlpatterns = [
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('placeorder/<int:order_id>/', views.order_review, name='order-review'),
]

