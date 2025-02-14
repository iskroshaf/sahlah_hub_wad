from django.shortcuts import render, redirect
from _authentication_app.decorators import redirect_authenticated_user
from _customer_app.forms import CustomerRegisterForm, ProfileUpdateForm

@redirect_authenticated_user
def customer_register_view(request):
    title = 'Register'
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.status = 'A'
            user.role = 'C'
            user.save()
            print('Register Successful')
            return redirect('login')  
        else:
            print(form.errors)
    else:
        form = CustomerRegisterForm()

    context = {'title': title, 'form': form}
    return render(request, '_customer_app/customer_register.html', context)

def customer_home_view(request):
    title = 'Customer Home'
    context = {'title': title}
    return render(request, '_customer_app/customer_home.html', context)


def user_profile(request):
    title = 'Profile'
    user = request.user
    form = ProfileUpdateForm(instance=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            print("Profile Updated")
            return redirect('profile')
        else:
            print(form.errors)
            form = ProfileUpdateForm(instance=user)
    context = {'title':title,'user':user,'form':form,'image_avatar':user.image_avatar.url}
    return render(request,'_customer_app/profile.html',context)