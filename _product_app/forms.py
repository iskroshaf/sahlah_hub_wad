from django import forms
from django.forms import ModelForm
from _product_app.models import Product, ProductCategory


class ProductCategoryForm(ModelForm):

    product_category_name = forms.CharField(
        label='Product Category Name: ',
        widget=forms.TextInput(attrs={'placeholder': 'Product Category Name','class':'form-control'}),
    )
            
    class Meta:
        model = ProductCategory
        fields = ['product_category_name']

class ProductForm(ModelForm):

    product_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Product Name'}),
    )

    product_price = forms.DecimalField(
        label='',
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'placeholder': 'Price'}),
    )

    product_category_name = forms.ModelChoiceField(
        label='',
        queryset=ProductCategory.objects.all(),  
        empty_label='Select Product Category',
        required=False
    )

    product_description = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description'})
    )

            
    class Meta:
        model = Product
        fields = ['product_name', 'product_price','product_category_name', 'product_description' ]