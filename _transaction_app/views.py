

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from _transaction_app.utils import refresh_transaction 
from json import JSONDecodeError
import requests
import re
import json
import logging
from .models import Transaction
from _order_app.models import Order
from _order_app.services import lock_and_deduct_stock
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages


def create_payment(request, order_id):
    
    order = get_object_or_404(
        Order, pk=order_id, status=Order.Status.PENDING
    )

  
    alamat = None
    if request.POST.get('alamat_id'):
        alamat = get_object_or_404(
            ShippingAddress,
            pk=request.POST['alamat_id'], 
            user=order.user,
        )

    bill_name  = (alamat.full_name if alamat else order.user.get_full_name())
    bill_phone = (alamat.phone if alamat else getattr(order.user, 'phone_number', ''))
    bill_phone = re.sub(r'\D', '', bill_phone)
    bill_email = order.user.email

  
    txn = order.transaction
    if not txn:
        txn = Transaction.objects.create(
            user   = order.user,
            amount = order.total_products + order.shipping_fee,
            status = Transaction.Status.PENDING,
        )
        order.transaction = txn
        order.save()


    payload = {
        'userSecretKey':    settings.TOYYIBPAY_SECRET_KEY,
        'categoryCode':     settings.TOYYIBPAY_CATEGORY_CODE,
        'billName':         f"Sahlan Order #{order.id}",
        'billDescription':  f"Pembayaran untuk order #{order.id} di Sahlan Hub",
        'billPriceSetting': 1,
        'billPayorInfo':    1,         
        'billTo': '',
        'billPaymentChannel': '',      
        'billAmount':       str(int(txn.amount * 100)),  
        'billChargeToCustomer':0,
        'billReturnUrl':    settings.TOYYIBPAY_RETURN_URL,
        'billCallbackUrl':  settings.TOYYIBPAY_CALLBACK_URL,

        'billTo':    bill_name,
        'billEmail': bill_email,
        'billPhone': bill_phone,
    }

    try:
        resp = requests.post(settings.TOYYIBPAY_API_URL, data=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()     
             
        if not (isinstance(data, list) and data and data[0].get("BillCode")):
            raise ValueError("BillCode not returned")

        bill_code = data[0]["BillCode"]
    # try:
    #     resp = requests.post(settings.TOYYIBPAY_API_URL, data=payload, timeout=15)
    #     print("ToyyibPay status:", resp.status_code)
    #     print("ToyyibPay body  :", resp.text[:300])   
    #     resp.raise_for_status()
    
    #     data = resp.json()                 
    except json.JSONDecodeError:
        print("Not JSON =>", resp.text)      
        return None

    except Exception as exc:
        txn.status = Transaction.Status.FAILED
        txn.save()
        return HttpResponse(f"ToyyibPay error: {exc}", status=502)
    
    txn.bill_code = bill_code
    txn.save()

    return redirect(f"https://dev.toyyibpay.com/{bill_code}")


        
@csrf_exempt
def payment_callback(request):
    logger = logging.getLogger(__name__)

    data = request.POST.dict()
    if not data:                     
        data = request.GET.dict()

    logger.info("CALLBACK DATA: %s", data)

    bill_code = data.get("billcode")
    status    = data.get("paymentStatus") or data.get("status_id")  

    if not bill_code:
        return HttpResponse("No billcode", status=400)

    txn   = get_object_or_404(Transaction, bill_code=bill_code)
    order = getattr(txn, "order", None)

    
    if status == "1":
        try:
            if order:
                logger.info("▶️ Order %s : mula tolak stok", order.id)
                lock_and_deduct_stock(order)          
                logger.info("✅ Order %s : stok dikemas kini", order.id)

            txn.mark_success()                       

            if order:
                order.status = Order.Status.PAID
                order.save(update_fields=["status"])

        except ValidationError as e:
            logger.error("Stock error: %s", e)
            txn.mark_failed()
            if order:
                order.status = Order.Status.FAILED
                order.save(update_fields=["status"])
            return HttpResponse(f"Stock error: {e}", status=422)

 
    elif status == "3":
        txn.status = Transaction.Status.FAILED
        if order:
            order.status = Order.Status.FAILED
            order.save(update_fields=["status"])

   
    else:
        txn.status = Transaction.Status.PENDING

    txn.save(update_fields=["status", "paid_at", "updated_at"])
    return HttpResponse("OK")


def payment_success(request):
    bill_code = request.GET.get('billcode')
    txn       = get_object_or_404(Transaction, bill_code=bill_code)
    order     = getattr(txn, "order", None)

    host = request.get_host()
    if "ngrok-free.app" in host:
       
        new_url = request.build_absolute_uri().replace(host, "localhost:8000")
        return redirect(new_url)

    if txn.status == Transaction.Status.PENDING:
        from _transaction_app.utils import refresh_transaction
        refresh_transaction(bill_code)
        txn.refresh_from_db()

  
    detail_url = reverse('order_detail', args=[order.id]) if order else '#'

    messages.success(request, "Order Accepted!")
    return render(request, "paymentSuccess.html", {
        "transaction":     txn,
        "order":           order,
        "redirect_seconds": 10,
        "detail_url":      detail_url,
    })

def payment_failed(request):
    bill_code = request.GET.get("billcode")
    txn   = get_object_or_404(Transaction, bill_code=bill_code)
    order = getattr(txn, "order", None)
    return render(request, "payment_failed.html",
                  {"order": order, "transaction": txn})
    