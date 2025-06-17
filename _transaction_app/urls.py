# _transaction_app/urls.py

from django.urls import path
from .views import create_payment, payment_callback, payment_success

urlpatterns = [
    path('payment/create/<int:order_id>/', create_payment,    name='payment-create'),
    path('payment/callback/',               payment_callback, name='payment-callback'),
    path('payment/success/',                payment_success,  name='payment-success'),
]
