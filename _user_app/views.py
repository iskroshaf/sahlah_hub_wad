from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from _user_app.decorators import redirect_authenticated_user
from _customer_app.forms import ProfileUpdateForm
from django.contrib import messages


def user_login(request):
    title = "Login"
    theme = "customer_theme"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Login Successful")
            if user.role == "C":
                return redirect("customer_home")
            else:
                if user.role == "S":
                    return redirect("seller_dashboard")
        else:
            print("Login Fail")
            messages.error(request, "Invalid username or password.")
    context = {"title": title, "theme": theme}
    return render(request, "_user_app/user_login.html", context)


def user_logout(request):
    logout(request)
    print("Logout Successful")
    return redirect("home")


def user_profile(request):
    title = "Profile"
    user = request.user
    form = ProfileUpdateForm(instance=user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            print("Profile Updated")
            return redirect("profile")
        else:
            print(form.errors)


    context = {
        "title": title,
        "user": user,
        "form": form,
    }
    return render(request, "_user_app/profile.html", context)
