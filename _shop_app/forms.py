import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator, MinValueValidator, MaxValueValidator,MinLengthValidator,MaxLengthValidator
from django.forms import ModelForm
from _shop_app.models import Shop


WORD_RE = re.compile(r"\b\w+\b")

def min_words(value, n=3, field="Field"):
    if len(WORD_RE.findall(value)) < n:
        raise ValidationError(f"{field} must contain at least {n} words.")


img_validator = FileExtensionValidator(
    ["jpg", "jpeg", "png"],
    message="Only .jpg, .jpeg or .png images are allowed."
)

address_validator = RegexValidator(
    regex=r'^[\w\s\-,.]+$',
    message='Address may only contain letters, numbers, spaces, commas, periods and dashes.'
)

alpha_space_validator = RegexValidator(
    regex=r'^[A-Za-z ]+$',
    message='This field may only contain letters and spaces.'
)

postcode_validator = RegexValidator(
    regex=r'^\d{5}$',
    message='Postcode must be exactly 5 digits, e.g. 76100.'
)

phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Enter a valid phone number (7–15 digits, optional leading +).'
)

class ShopForm(ModelForm):
    shop_name = forms.CharField(
        label="Shop Name",
        error_messages={'required': 'Shop name is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your shop name',
            'class': 'form-control',
        })
    )

    shop_phone_number = forms.CharField(
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'placeholder': '+60123456789',
            'class': 'form-control',
            'maxlength': '15',
            'minlength': '7',
            'inputmode': 'numeric',
        })
    )

    shop_category = forms.CharField(
        error_messages={'required': 'Shop category is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Shop category',
            'class': 'form-control',
        })
    )

    shop_desc = forms.CharField(
        required=True,
        min_length=10,
        max_length=250,
        validators=[
            MinLengthValidator(10, message='Description must be at least 10 characters.'),
            MaxLengthValidator(250, message='Description cannot exceed 250 characters.'),
        ],
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Describe your shop (10–250 characters)',
            'class': 'form-control',
        })
    )


    shop_address_1 = forms.CharField(
        required=True,
        max_length=255,
        validators=[address_validator],
        error_messages={'required': 'Address line 1 is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Address line 1',
            'class': 'form-control',
        })
    )
    shop_address_2 = forms.CharField(
        required=False,
        max_length=255,
        validators=[address_validator],
        widget=forms.TextInput(attrs={
            'placeholder': 'Address line 2 (optional)',
            'class': 'form-control',
        })
    )
    shop_city = forms.CharField(
        required=True,
        max_length=50,
        validators=[alpha_space_validator],
        error_messages={'required': 'City is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-control',
        })
    )
    shop_state = forms.CharField(
        required=True,
        max_length=50,
        validators=[alpha_space_validator],
        error_messages={'required': 'State is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'State',
            'class': 'form-control',
        })
    )
    shop_postcode = forms.CharField(
        required=True,
        max_length=10,
        validators=[postcode_validator],
        error_messages={'required': 'Postcode is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Postcode',
            'class': 'form-control',
        })
    )


    shop_logo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={'invalid_image': 'Uploaded logo must be a valid image.'},
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    shop_bg_photo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={'invalid_image': 'Uploaded background must be a valid image.'},
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Shop
        fields = [
            'shop_name',
            'shop_phone_number',
            'shop_category',
            'shop_desc',
            'shop_address_1',
            'shop_address_2',
            'shop_city',
            'shop_state',
            'shop_postcode',
            'shop_logo',
            'shop_bg_photo',
        ]

    def clean(self):
        cleaned = super().clean()
        addr1 = cleaned.get('shop_address_1', '')
        addr2 = cleaned.get('shop_address_2', '')
        if addr2 and len(addr2) > len(addr1):
            self.add_error('shop_address_2', 
                'Address line 2 cannot be longer than line 1.')
        return cleaned


class ShopUpdateForm(ModelForm):
    shop_name = forms.CharField(
        required=True,
        max_length=50,
        error_messages={'required': 'Shop name is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your shop name',
            'class': 'form-control',
        })
    )

    shop_category = forms.CharField(
        required=True,
        max_length=50,
        error_messages={'required': 'Shop category is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Shop category',
            'class': 'form-control',
        })
    )

    shop_phone_number = forms.CharField(
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'id': 'id_shop_phone_number',
            'placeholder': '+60123456789',
            'class': 'form-control',
            'maxlength': '11',
            'minlength': '7',
            'inputmode': 'numeric',
        })
    )
    shop_desc = forms.CharField(
        required=True,
        min_length=10,
        max_length=250,
        validators=[
            MinLengthValidator(10, message='Description must be at least 10 characters.'),
            MaxLengthValidator(250, message='Description cannot exceed 250 characters.'),
        ],
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Describe your shop (10–250 characters)',
            'class': 'form-control',
        })
    )

    shop_address_1 = forms.CharField(
        required=True,
        max_length=255,
        validators=[address_validator],
        error_messages={'required': 'Address line 1 is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Address line 1',
            'class': 'form-control',
        })
    )

    shop_address_2 = forms.CharField(
        required=False,
        max_length=255,
        validators=[address_validator],
        widget=forms.TextInput(attrs={
            'placeholder': 'Address line 2 (optional)',
            'class': 'form-control',
        })
    )

    shop_city = forms.CharField(
        required=True,
        max_length=50,
        validators=[alpha_space_validator],
        error_messages={'required': 'City is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-control',
        })
    )

    shop_state = forms.CharField(
        required=True,
        max_length=50,
        validators=[alpha_space_validator],
        error_messages={'required': 'State is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'State',
            'class': 'form-control',
        })
    )

    shop_postcode = forms.CharField(
        required=True,
        max_length=10,
        validators=[postcode_validator],
        error_messages={'required': 'Postcode is required.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Postcode',
            'class': 'form-control',
        })
    )

    # Logo & banner unchanged
    shop_logo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={'invalid_image': 'Uploaded logo must be a valid image.'},
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    shop_bg_photo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={'invalid_image': 'Uploaded background must be a valid image.'},
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    # Rating & delivery_fee left commented out for later use
    # shop_rating = ...
    # shop_delivery_fee = ...

    class Meta:
        model = Shop
        fields = [
            'shop_name',
            'shop_category',
            'shop_phone_number',
            'shop_desc',
            'shop_address_1',
            'shop_address_2',
            'shop_city',
            'shop_state',
            'shop_postcode',
            'shop_logo',
            'shop_bg_photo',
        ]

    def clean(self):
        cleaned = super().clean()
        addr1 = cleaned.get('shop_address_1', '')
        addr2 = cleaned.get('shop_address_2', '')
        if addr2 and len(addr2) > len(addr1):
            self.add_error('shop_address_2',
                           'Address line 2 cannot be longer than line 1.')
        return cleaned
