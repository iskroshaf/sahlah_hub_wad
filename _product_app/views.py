from django.shortcuts import render

def product_list_view(request):
    title = 'My Product'
    context = {'title': title}
    return render(request,'_product_app/product_list.html',context)