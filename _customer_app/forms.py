from datetime import datetime
from django import forms
from django.forms import FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from _user_app.models import CustomUser
from _customer_app.models import Customer
from django.core.exceptions import ValidationError
from datetime import date



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
        choices=CustomUser.GENDER_CHOICES,  # Fixed missing model reference
        widget=forms.RadioSelect,
        required=False,
    )
    phone_number=forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Phone Number"}),
    )

    image_avatar = forms.ImageField(widget=FileInput, required=False)

    class Meta:
        model = CustomUser  # Fixed missing model reference
        fields = ("first_name", "last_name", "birthdate", "gender", "phone_number", "image_avatar")

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 18:
                raise ValidationError("You must be at least 18 years old.")

        return birthdate
