import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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

class ShopForm(ModelForm):

    shop_name = forms.CharField(
        label="Shop Name",
        error_messages={"required": "Shop name is required."},
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your shop name", "class": "form-control"
        })
    )

    shop_phone_number = forms.CharField(
        error_messages={
            "required": "Shop phone number is required."
        },
        widget=forms.TextInput(attrs={
            "placeholder": "0123456789", "class": "form-control",
            "maxlength": "11", "minlength": "9", "inputmode": "numeric",
        })
    )

    shop_logo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={
            "invalid_image": "Uploaded logo must be a valid image.",
        },
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    shop_bg_photo = forms.ImageField(
        required=False,
        validators=[img_validator],
        error_messages={
            "invalid_image": "Uploaded background must be a valid image."
        },
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    shop_category = forms.CharField(
        error_messages={"required": "Shop category is required."},
        widget=forms.TextInput(attrs={
            "placeholder": "Shop category", "class": "form-control"
        })
    )

    shop_desc = forms.CharField(
        error_messages={"required": "Shop description is required."},
        widget=forms.Textarea(attrs={
            "rows": 3, "placeholder": "Describe your shop (≥ 3 words)",
            "class": "form-control"
        })
    )

    # ---------- Address ----------
    shop_address_1 = forms.CharField(
        error_messages={"required": "Shop address line 1 is required."},
        widget=forms.TextInput(attrs={
            "placeholder": "Address line 1", "class": "form-control"
        })
    )

    shop_address_2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Address line 2 (optional)", "class": "form-control"
        })
    )

    shop_city = forms.CharField(
        error_messages={"required": "City is required."},
        widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"})
    )

    shop_state = forms.CharField(
        error_messages={"required": "State is required."},
        widget=forms.TextInput(attrs={"placeholder": "State", "class": "form-control"})
    )

    shop_postcode = forms.CharField(
        error_messages={"required": "Postcode is required."},
        widget=forms.TextInput(attrs={"placeholder": "Postcode", "class": "form-control"})
    )

    class Meta:
        model = Shop
        fields = [
            "shop_name", "shop_bg_photo", "shop_logo", "shop_phone_number",
            "shop_category", "shop_desc",
            "shop_address_1", "shop_address_2",
            "shop_city", "shop_state", "shop_postcode",
        ]

    # ---------- Custom validators ----------
    def clean_shop_desc(self):
        desc = self.cleaned_data["shop_desc"].strip()
        min_words(desc, 3, "Description")
        return desc

    def clean_shop_phone_number(self):
        phone = self.cleaned_data["shop_phone_number"].strip()
        if not re.fullmatch(r"\d{9,11}", phone):
            raise ValidationError(
                "Phone number must be 9–11 digits and contain digits only."
            )
        return phone
