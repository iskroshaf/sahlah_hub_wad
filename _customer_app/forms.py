from datetime import datetime
from django import forms
from django.forms import FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from _authentication_app.models import CustomUser
from _customer_app.models import Customer

class CustomerRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
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
        model = Customer  # Fixed missing model reference
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )

    birthdate = forms.DateField(
        label='',
        widget=forms.SelectDateWidget(
            years=range(1950, datetime.now().year + 1),
            empty_label=("Year", "Month", "Day")
        ),
        required=False,
    )

    gender = forms.ChoiceField(
        label='',
        choices=CustomUser.GENDER_CHOICES,  # Fixed missing model reference
        widget=forms.RadioSelect,
        required=False
    )

    image_avatar = forms.ImageField(
        widget=FileInput,
        required=False
    )

    class Meta:
        model = CustomUser  # Fixed missing model reference
        fields = ('first_name', 'last_name', 'birthdate', 'gender', 'image_avatar')
