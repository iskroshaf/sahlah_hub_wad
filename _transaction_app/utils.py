import requests,json
from django.utils import timezone
from .models import Transaction
from _order_app.models import Order   

TOYYIB_GET_TXN = "https://dev.toyyibpay.com/index.php/api/getBillTransactions"   

def refresh_transaction(bill_code):
    
    payload = {"billCode": bill_code}          
    try:
        resp = requests.post(TOYYIB_GET_TXN, data=payload, timeout=15)
        print("RAW RESPONSE:", resp.text[:200])
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("ToyyibPay pull error:", e)
        return None

    if not data:
        return None

    info = data[0]
    status_code = info.get("billpaymentStatus")     

    status_map = {
        "1": Transaction.Status.SUCCESS,
        "2": Transaction.Status.PENDING,
        "3": Transaction.Status.FAILED,
        "4": Transaction.Status.PENDING,
    }

    txn = Transaction.objects.filter(bill_code=bill_code).first()
    if not txn:
        return info

    new_status = status_map.get(status_code)
    if new_status and new_status != txn.status:
        txn.status = new_status
        if new_status == Transaction.Status.SUCCESS:
            txn.paid_at = timezone.now()
        txn.save()

        # selaraskan Order sekali
        try:
            order = txn.order
            if new_status == Transaction.Status.SUCCESS:
                order.status = Order.Status.PAID
            elif new_status == Transaction.Status.FAILED:
                order.status = Order.Status.FAILED
            order.save()
        except Order.DoesNotExist:
            pass

    return info