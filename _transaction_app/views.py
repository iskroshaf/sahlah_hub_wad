# _transaction_app/views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import requests

from .models import Transaction
from _order_app.models import Order

def create_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    transaction = Transaction.objects.create(
        user=order.user,
        gateway='toyyibpay',
        amount=order.total_products + order.shipping_fee,
    )
    payload = {
        'userSecretKey':     settings.TOYYIBPAY_SECRET_KEY,
        'categoryCode':      settings.TOYYIBPAY_CATEGORY_CODE,
        'billName':          f"Sahlan Order #{order.id}",
        'billDescription':   f"Pembayaran untuk order #{order.id} di Sahlan Hub",
        'billPriceSetting':  0,
        'billPayorInfo':     0,
        'billPaymentChannel': "",
        'billAmount':        str(int(transaction.amount * 100)),
        'billReturnUrl':     settings.TOYYIBPAY_RETURN_URL,
        'billCallbackUrl':   settings.TOYYIBPAY_CALLBACK_URL,
        'billTo':            order.user.get_full_name() if order.user else "",
        'billEmail':         order.user.email if order.user else "",
        'billPhone':         request.POST.get('phone', ''),
    }
    resp = requests.post(
        settings.TOYYIBPAY_API_URL,  # https://dev.toyyibpay.com/index.php/api/createBill
        data=payload
    )
    try:
        resp = requests.post(settings.TOYYIBPAY_API_URL, data=payload)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            bill_code = data[0].get('BillCode')
            if bill_code:
                transaction.bill_code = bill_code
                transaction.save()
                return redirect(f"{settings.TOYYIBPAY_BASE_URL}/{bill_code}")
        transaction.status = Transaction.Status.FAILED
        transaction.save()
        return HttpResponse("Failed to create bill", status=500)
    except Exception as e:
        transaction.status = Transaction.Status.FAILED
        transaction.save()
        return HttpResponse(f"Error: {str(e)}", status=500)

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        status_id   = request.POST.get('status_id')
        bill_code   = request.POST.get('billcode')
        paid_amount = request.POST.get('paid_amount')
        try:
            transaction = Transaction.objects.get(bill_code=bill_code)
            if status_id == '2':
                transaction.status = Transaction.Status.SUCCESS
            elif status_id == '3':
                transaction.status = Transaction.Status.FAILED
            else:
                transaction.status = Transaction.Status.PENDING
            transaction.save()
            return HttpResponse('OK')
        except Transaction.DoesNotExist:
            return HttpResponse('Transaction not found', status=404)
    return HttpResponse('Method not allowed', status=405)

def payment_success(request):
    return render(request, 'paymentSuccess.html')
