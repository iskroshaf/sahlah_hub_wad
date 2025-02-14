from django.shortcuts import redirect, render

from _shop_app.forms import RestaurantForm


def shop_register_view(request):
    title = 'Shop Register'
    form = RestaurantForm()

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user.seller
            restaurant = form.save(commit=False)
            restaurant.seller = seller  
            restaurant.save()  

            print('Restaurant Register Successful')
            return redirect('shop_register')
        else:
            print(form.errors)

    context = {'title': title, 'form': form,}
    return render(request, '_shop_app/shop_register.html', context)
