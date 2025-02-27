from django import forms
from django.forms import ModelForm, FileInput

from _shop_app.models import Shop


class ShopForm(ModelForm):
    shop_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Shop Name'}),
        )
    
    shop_bg_photo = forms.ImageField(
        label= '',
        widget=FileInput,
        required=False
        )
    
    shop_logo = forms.ImageField(
        label= '',
        widget=FileInput,
        required=False
        )
    
    shop_phone_number = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number (e.g., 0123456789)'}),
        )
    
    
    shop_desc = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'rows': 3,'placeholder': 'Description'})
        )
    
    shop_category = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Category'}),
        )
    
    class Meta:
        model = Shop
        fields = ['shop_name', 'shop_bg_photo','shop_phone_number','shop_category','shop_logo','shop_desc']