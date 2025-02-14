from django import forms
from django.contrib.auth.forms import UserCreationForm

from _seller_app.models import Seller

class SellerRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='',
        # required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
        )

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
        )
    
    phone_number = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Phone No'})
        )
    
    business_license = forms.FileField(
        label='',
        required=True,
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
        )
    
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        )
    
    class Meta:
        model = Seller
        fields = ['username', 'email', 'phone_number' , 'business_license', 'password1', 'password2']


