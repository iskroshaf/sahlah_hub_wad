from django.shortcuts import redirect
from django.urls import reverse

def redirect_authenticated_user(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return function(request, *args, **kwargs)
    return wrapper
