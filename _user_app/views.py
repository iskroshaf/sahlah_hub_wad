from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from _user_app.decorators import redirect_authenticated_user
from _customer_app.forms import ProfileUpdateForm

def user_login(request):
    title = 'Login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            print('Login Successful')
            if user.role == 'C':
                return redirect('customer_home')  
            else:
                if user.role == 'S':
                    return redirect('seller_dashboard')
        else:
            print('Login Fail')
    context = {'title': title}
    return render(request, '_user_app/user_login.html', context)

def user_logout(request):
    logout(request)
    print('Logout Successful')
    return redirect('login')

def user_profile(request):
    title = 'Profile'
    user = request.user
    form = ProfileUpdateForm(instance=user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            print("Profile Updated")
            return redirect('profile')
        else:
            print(form.errors)

    image_avatar = user.image_avatar.url if user.image_avatar else None
    
    context = {'title': title, 'user': user, 'form': form, 'image_avatar': image_avatar}
    return render(request, '_user_app/profile.html', context)
