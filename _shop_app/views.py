from django.shortcuts import render

def shop_register_view(request):
    title = 'Shop Register'
    context = {'title': title} 
    return render(request, '_shop_app/shop_register.html')
