from django import forms
from django.forms import ModelForm, FileInput

from _shop_app.models import Restaurant


class RestaurantForm(ModelForm):
    restaurant_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Restaurant Name'}),
        )
    
    restaurant_bg_photo = forms.ImageField(
        label= '',
        widget=FileInput,
        required=False
        )
    
    restaurant_logo = forms.ImageField(
        label= '',
        widget=FileInput,
        required=False
        )
    
    restaurant_phone_number = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number (e.g., 0123456789)'}),
        )
    
    
    restaurant_desc = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'rows': 3,'placeholder': 'Description'})
        )
    
    restaurant_category = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Category'}),
        )
    
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_bg_photo','restaurant_phone_number','restaurant_category','restaurant_logo','restaurant_desc']