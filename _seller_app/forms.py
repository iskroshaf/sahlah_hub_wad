from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from _seller_app.models import Seller



phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Enter a valid phone number (7–15 digits, optional +).'
)


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


class SellerProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    phone_number = forms.CharField(
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': '+60123456789'
        })
    )
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type':'date',
            'class':'form-control'
        })
    )
    gender = forms.ChoiceField(
        required=False,
        choices=Seller.GENDER_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    image_avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class':'form-control'})
    )
    business_license = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = Seller
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'birthdate', 'gender',
            'image_avatar', 'business_license'
        ]


