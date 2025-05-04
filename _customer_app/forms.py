from datetime import datetime
from django import forms
from django.forms import FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from _user_app.models import CustomUser
from _customer_app.models import Customer,ShippingAddress
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from datetime import date
import re
from django.contrib.auth import authenticate



class CustomerRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Username"})
    )

    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "input-password", "placeholder": "Password"}
        ),
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "input-password", "placeholder": "Confirm Password"}
        ),
    )

    class Meta:
        model = Customer  # Fixed missing model reference
        fields = ["username", "email", "password1", "password2"]
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose another one.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use another email.")
        return email
    


class ProfileUpdateForm(UserChangeForm):
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )

    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    birthdate = forms.DateField(
        label="",
        widget=forms.SelectDateWidget(
            years=range(1950, datetime.now().year + 1),
            empty_label=("Year", "Month", "Day"),
        ),
        required=False,
    )

    gender = forms.ChoiceField(
        label="",
        choices=CustomUser.GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Phone Number"}),
    )

    image_avatar = forms.ImageField(
        widget=FileInput,
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "birthdate", "gender", "phone_number", "image_avatar")

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 18:
                raise ValidationError("You must be at least 18 years old.")

        return birthdate



class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password"})
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if not self.user.check_password(current_password):
            self.add_error('current_password', "The current password is incorrect.")

        if new_password != confirm_password:
            self.add_error('confirm_password', "The two password fields must match.")

        password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if new_password and not re.match(password_regex, new_password):
            self.add_error('new_password', "Password must be at least 8 characters, contain one uppercase letter, one number, and one special character.")

        return cleaned_data

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'phone',
            'address_line1', 'address_line2',
            'city', 'state', 'postcode', 'country'
        ]
