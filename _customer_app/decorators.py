
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from _customer_app.models import ShippingAddress

def customer_requirements_complete(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and getattr(user, "role", None) == "C":
            # 1) Profile lengkap?
            missing_profile = (
                not user.first_name or
                not user.phone_number or
                not user.birthdate
            )
            if missing_profile:
                messages.warning(
                    request,
                    "Please fill all the required profile information."
                )
                return redirect("Update_profile")

            
            if not ShippingAddress.objects.filter(user=user).exists():
                messages.warning(
                    request,
                    "Please add at least one shipping address before continuing."
                )
                return redirect("customer_update_address")

        return view_func(request, *args, **kwargs)
    return _wrapped