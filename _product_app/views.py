from django.shortcuts import get_object_or_404, redirect, render

from _product_app.forms import ProductCategoryForm
from _product_app.models import ProductCategory
from _shop_app.models import Shop

def product_category_management_view(request, pk):
    title = 'Product Category'
    shop = get_object_or_404(Shop, shop_id=pk)
    product_categories = ProductCategory.objects.filter(shop=shop)

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        
        if form.is_valid():
            product_category_name = form.cleaned_data['product_category_name']
            product_category = ProductCategory(
                product_category_name=product_category_name,
                shop=shop
            )
            product_category.save()
            product_category.auto_translate(fields=['product_category_name'])

            return redirect('product_category_management', pk=shop.shop_id)
    else:
        form = ProductCategoryForm()
    context = {
        'title': title,
        'shop': shop,
        'form': form,
        'product_categories': product_categories,
    }

    return render(request, '_product_app/product_category_management.html', context)



def product_list_view(request, pk):
    title = 'My Product'
    shop = get_object_or_404(Shop, shop_id = pk)
    context = {'title': title, 'shop': shop}
    return render(request,'_product_app/product_list.html',context)