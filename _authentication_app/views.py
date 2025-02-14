from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from _authentication_app.decorators import redirect_authenticated_user

@redirect_authenticated_user
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
    return render(request, '_authentication_app/user_login.html', context)

def user_logout(request):
    logout(request)
    print('Logout Successful')
    return redirect('login')
