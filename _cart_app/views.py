# _cart_app/views.py
import json
from decimal import Decimal
from collections import defaultdict

from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction

from .services import (add_to_cart,set_quantity,get_items,_get_cart,cart_total as cart_total_fn,)
from _product_app.models import ProductVariant
from _delivery_app.models import DeliveryMethod
from _order_app.models import Order, OrderItem,OrderShipping
from _transaction_app.models import Transaction
from .utils import clamp_cart



@require_POST
def add_to_cart_view(request):
   
   
    variant_id = request.POST["variant_id"]
    qty = int(request.POST.get("quantity", request.POST.get("qty", 1)))

   
    shop_pk = ProductVariant.objects.get(pk=variant_id).product.shop.pk
    chosen_dm = request.POST.get("delivery_method_id", "")

    ship_sel = request.session.get("ship_sel", {})  
    ship_sel[str(shop_pk)] = chosen_dm
    request.session["ship_sel"] = ship_sel

    add_to_cart(request, variant_id, qty)
    messages.success(request, "Add to the Cart!")
    return redirect("cart:view")



@require_POST
def ajax_set_qty(request, variant_id):
    data = json.loads(request.body or "{}")
    qty = int(data.get("qty", 0))
    try:
        item = set_quantity(request, variant_id, qty) 
        total = cart_total_fn(request)
        if item is None:
            return JsonResponse({"total": f"{total:.2f}"})

        subtotal = item.quantity * item.variant.variant_price
        return JsonResponse(
            {
                "quantity": item.quantity,
                "subtotal": f"{subtotal:.2f}",
                "total": f"{total:.2f}",
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_POST
def ajax_remove_item(request, variant_id):
    set_quantity(request, variant_id, 0)
    return JsonResponse({"total": f"{cart_total_fn(request):.2f}"})



def cart_page(request):
 
    qs = get_items(request)
    clamp_cart(request, _get_cart(request))
    theme = "customer_theme"
    cart_items = [
        {
            "variant":  it.variant,
            "quantity": it.quantity,
            "subtotal": it.quantity * it.variant.variant_price,
            "shop":     it.variant.product.shop,
        }
        for it in qs
    ]
    cart_sum = cart_total_fn(request)

    
    shop_blocks = defaultdict(list)
    for it in cart_items:
        shop_blocks[it["shop"]].append(it)

   
    selected_map = request.session.get("ship_sel", {})   
    shops_data   = []
    grand_ship_fee = Decimal("0.00")

    for shop, items in shop_blocks.items():

        if shop.delivery_price_type == "custom" and shop.shop_delivery_fee:
      
            methods = []                     
            sel_id  = ""                      
            fee_sel = shop.shop_delivery_fee  
        else:
           
            methods = DeliveryMethod.objects.filter(is_active=True).order_by("id")
            sel_id  = (
                selected_map.get(str(shop.pk))
                or (str(methods.first().pk) if methods else "")
            )
            fee_sel = next(
                (m.base_price for m in methods if str(m.pk) == sel_id),
                Decimal("0.00"),
            )

        grand_ship_fee += fee_sel

        shops_data.append(
            {
                "shop":         shop,
                "methods":      methods,     
                "selected_id":  sel_id,      
                "selected_fee": fee_sel,     
            }
        )

    return render(
        request,
        "cart.html",
        {
            'theme': 'customer_theme',
            "cart_items": cart_items,
            "cart_total": cart_sum,
            "shops_data": shops_data,
            "grand_fee":  grand_ship_fee,
        },
    )



@require_POST
@transaction.atomic
def checkout(request):

    if request.user.role != "C":
        raise ValueError("only customer allowed")

    cart = _get_cart(request)
    if not cart.items.exists():
        messages.error(request, "Troli kosong.")
        return redirect("cart:view")
    
    if clamp_cart(request, cart):    
        return redirect("cart:view")


  
    sel_map = {
        k.replace("ship_sel_", ""): v                    
        for k, v in request.POST.items()
        if k.startswith("ship_sel_") and v                
    }

 
    flat_map = {
        k.replace("flat_fee_shop", ""): Decimal(v)        
        for k, v in request.POST.items()
        if k.startswith("flat_fee_shop")
    }

   
    total_ship_fee = Decimal("0.00")


    methods_chosen = []
    for dm_pk in sel_map.values():
        dm = get_object_or_404(DeliveryMethod, pk=dm_pk)
        total_ship_fee += dm.base_price
        methods_chosen.append(dm)


    total_ship_fee += sum(flat_map.values())


    order = Order.objects.create(
        user          = request.user if request.user.is_authenticated else None,
        session_key   = request.session.session_key,
        shipping_fee  = total_ship_fee,
        total_products= cart_total_fn(request),
        status         = Order.Status.PENDING,
    )

   
    OrderItem.objects.bulk_create([
        OrderItem(
            order      = order,
            variant    = ci.variant,
            quantity   = ci.quantity,
            unit_price = ci.variant.variant_price,
        )
        for ci in cart.items.select_related("variant")
    ])

   
    shipping_rows = []

   
    for shop_pk, dm_pk in sel_map.items():
        dm = DeliveryMethod.objects.get(pk=dm_pk)
        shipping_rows.append(
            OrderShipping(
                order    = order,
                shop_id  = shop_pk,
                method   = dm,
                fee      = dm.base_price,
            )
        )

   
    for shop_pk, fee in flat_map.items():
        shipping_rows.append(
            OrderShipping(
                order    = order,
                shop_id  = shop_pk,
                method   = None,   
                fee      = fee,
            )
        )

    OrderShipping.objects.bulk_create(shipping_rows)

    txn = Transaction.objects.create(
        user   = order.user,
        amount = order.total_products + order.shipping_fee,
        status = Transaction.Status.PENDING,
    )
    order.transaction = txn
    order.save()

  
    cart.items.all().delete()
    messages.success(request, "Order Accepted!")
    return redirect('order-review', order_id=order.id)




