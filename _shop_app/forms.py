from django import forms
from django.forms import ModelForm, FileInput

from _shop_app.models import Shop


class ShopForm(ModelForm):
    shop_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your shop name", "class": "form-control"}
        ),
    )

    shop_bg_photo = forms.ImageField(
        label="",
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False,
    )

    shop_logo = forms.ImageField(
        label="",
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False,
    )

    shop_phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your phone number (e.g., 0123456789)", "class": "form-control"}
        ),
    )

    shop_desc = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Enter a brief shop description", "class": "form-control"}
        ),
    )

    shop_category = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Enter your shop category", "class": "form-control"}),
    )

    shop_address_1 = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your shop address (Line 1)", "class": "form-control"}
        ),
    )

    shop_address_2 = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your shop address (Line 2)", "class": "form-control"}
        ),
    )

    shop_city = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your city", "class": "form-control"}
        ),
    )

    shop_state = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your state", "class": "form-control"}
        ),
    )

    shop_postcode = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your postcode", "class": "form-control"}
        ),
    )

    # shop_country = forms.CharField(
    #     label="",
    #     widget=forms.TextInput(
    #         attrs={"placeholder": "Enter your country", "class": "form-control"}
    #     ),
    # )

    class Meta:
        model = Shop
        fields = [
            "shop_name",
            "shop_bg_photo",
            "shop_logo",
            "shop_phone_number",
            "shop_category",
            "shop_desc",
            "shop_address_1",
            "shop_address_2",
            "shop_city",
            "shop_state",
            "shop_postcode",
            # "shop_country",
        ]
