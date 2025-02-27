from django.shortcuts import redirect, render

from _shop_app.forms import ShopForm


def shop_register_view(request):
    title = 'Shop Register'
    form = ShopForm()

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user.seller
            shop = form.save(commit=False)
            shop.seller = seller  
            shop.save()  

            print('Shop Register Successful')
            return redirect('shop_register')
        else:
            print(form.errors)

    context = {'title': title, 'form': form,}
    return render(request, '_shop_app/shop_register.html', context)
