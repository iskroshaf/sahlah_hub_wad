from django.shortcuts import render, redirect
from _customer_app.forms import CustomerRegisterForm
from django.contrib import messages
 


def customer_register_view(request):
    title = "Register"
    theme = "customer_theme"
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = "A"
            user.role = "C"
            user.save()
            print("Register Successful")
            return redirect("login")
        else:
            # print(form.errors)
             if form.errors.get('email'):
                messages.error(request, f"Error with email: {form.errors['email'][0]}")  # Mesej ralat email
             elif form.errors.get('password2'):
                messages.error(request, f"Error with password confirmation: {form.errors['password2'][0]}")  # Mesej ralat password

    else:
        form = CustomerRegisterForm()

    context = {"title": title, "theme": theme, "form": form}
    return render(request, "_customer_app/customer_register.html", context)


def customer_home_view(request):
    title = "Customer Home"
    theme = "customer_theme"
    context = {"title": title, 'theme': theme}
    return render(request, "_customer_app/customer_home.html", context)
