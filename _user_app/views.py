from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from _user_app.decorators import redirect_authenticated_user
from _customer_app.forms import ProfileUpdateForm
from django.contrib import messages


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

            if user.role == "S":
                if user.status == "I":
                    messages.error(
                        request,
                        "Akaun seller anda sudah dinyahaktifkan."
                    )
                    return redirect("login")

            if user.role == "A" and not user.is_staff:
                user.is_staff = True
                user.save(update_fields=["is_staff"])

            if user.role == "C" and user.status == "I":
                messages.error(
                    request,
                    "Akaun anda telah dinyahaktifkan. Hubungi sokongan jika ini satu kesilapan."
                )
                return redirect("login")

            if user.role == "C":
                missing = (
                    not user.first_name or
                    not user.phone_number or
                    not user.birthdate  
                )
                if missing:
                    return redirect("Update_profile")
                return redirect("customer_home")

            elif user.role == "S":
                return redirect("seller_dashboard")
            elif user.role == "A":
                return redirect("admin_dashboard")
            else:
              
                logout(request)
                messages.error(request, "Anda tidak mempunyai akses.")
                return redirect("login")

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
        "theme": "customer_theme",
    }
    return render(request, "_user_app/profile.html", context)



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
