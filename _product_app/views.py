from django.shortcuts import get_object_or_404, render

from _shop_app.models import Shop

def product_list_view(request,pk):
    title = 'My Product'
    shop = get_object_or_404(Shop, shop_id = pk)
    context = {'title': title, 'shop': shop}
    return render(request,'_product_app/product_list.html',context)