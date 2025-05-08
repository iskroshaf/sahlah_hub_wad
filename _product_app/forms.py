from django import forms
from django.forms import ModelForm,IntegerField
from _product_app.models import Product, ProductCategory



class ProductCategoryForm(ModelForm):

    product_category_name = forms.CharField(
        label="Product Category Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Product Category Name",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = ProductCategory
        fields = ["product_category_name"]


class ProductForm(ModelForm):

    product_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Product Name", "class": "form-control"}
        ),
    )

    product_price = forms.DecimalField(
        label="",
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"placeholder": "Price", "class": "form-control"}),
    )

    product_quantity = IntegerField(
        label="",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Quantity", "class": "form-control"}),
    )

    product_category_name = forms.ModelChoiceField(
        label="",
        queryset=ProductCategory.objects.all(),
        empty_label="Select Product Category",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    product_description = forms.CharField(
        label="",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Description",  "class": "form-control"}),
    )

    product_image = forms.ImageField(
        label="",
        widget=forms.FileInput(attrs={"class": "form-control", "id": "change-product-image"}),
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "product_name",
            "product_price",
            "product_category_name",
            "product_description",
            "product_image"
        ]
