from django import forms
from django.forms import ModelForm
from _product_app.models import ProductCategory


class ProductCategoryForm(ModelForm):

    product_category_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Product Category Name'}),
    )
            
    class Meta:
        model = ProductCategory
        fields = ['product_category_name']