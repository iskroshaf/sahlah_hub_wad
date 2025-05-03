from django.shortcuts import render, redirect
from _customer_app.forms import CustomerRegisterForm,ProfileUpdateForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash 

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


def customer_update_profile(request):
    title = "Update Profile"
    theme = "customer_theme"
    context = {"title": title, "theme": theme}
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            current_password = cleaned_data.get("current_password")
            new_password = cleaned_data.get("new_password")

            if current_password and new_password:
                if not user.check_password(current_password):
                    form.add_error('current_password', 'The current password is incorrect.')
                    context['form'] = form
                    return render(request, "_customer_app/customer_update_profile.html", context)
                user.set_password(new_password)

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("customer_home")
        else:
            context['form'] = form
    else:
        form = ProfileUpdateForm(instance=user)

    context['form'] = form
    return render(request, "_customer_app/customer_update_profile.html", context)



from django.contrib.auth import update_session_auth_hash  # pastikan import ini ada


def customer_update_password(request):
    title = "Change Password"
    theme = "customer_theme"
    context = {"title": title, "theme": theme}

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # supaya user tak logout
            messages.success(request, "Password updated successfully!")
            return redirect("customer_home")
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, "_customer_app/customer_update_password.html", context)


