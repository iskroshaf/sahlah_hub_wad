from django import forms
from django.forms import ModelForm,IntegerField,inlineformset_factory
from _product_app.models import Product, ProductCategory,ProductVariant
from django.core.exceptions import ValidationError
from parler.forms import TranslatableModelForm


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


# class ProductForm(ModelForm):
class ProductForm(TranslatableModelForm):

    PRODUCT_STATUS_CHOICES = [
    ('', 'Select status'),
    ('available', 'Available'),
    ('non-available', 'Non-Available'),
    ]

    product_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Product Name", "class": "form-control"}),
        error_messages={
            'required': 'Name of product is required .',
        }
        
    )

    product_price = forms.DecimalField(
        label="",
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Price", "class": "form-control"}),
        error_messages={
            'required': 'Price is required.',
            'min_value': 'Price must be at least RM0.01.',
        }
    )

    # product_quantity = IntegerField(
    #     label="",
    #     min_value=0,
    #     widget=forms.NumberInput(attrs={"placeholder": "Quantity", "class": "form-control"}),
    #     error_messages={
    #     'required': 'Please insert a quantity of product.',   
    # }
    # )

    product_category_name = forms.ModelChoiceField(
        label="",
        queryset=ProductCategory.objects.all(),
        empty_label="Select Product Category",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={
        'required': 'Please Choose a Category of Product.',   
    }
    )

    product_description = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Description",  "class": "form-control"}),
    )

    product_image = forms.ImageField(
        label="",
        widget=forms.FileInput(attrs={"class": "form-control", "id": "change-product-image"}),
        required=False,
        error_messages={
            'required': 'Please upload at least 1 ',
        }
    )

    product_availability = forms.ChoiceField(
        label="",
        choices=PRODUCT_STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={
            'required': 'Please choose availability ',
        }
    )
    no_variant = forms.BooleanField(
        required=False,
        label="Tiada varian (satu harga & stok sahaja)",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    base_quantity = forms.IntegerField(
        label="Stok (jika tiada varian)",
        min_value=0,
        required=False,                      # hanya wajib bila no_variant=True
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )


    class Meta:
        model = Product
        fields = [
            "product_name",
            "product_category_name",
            "product_description",
            "product_image",
            "product_availability",
        ]
    
        labels = {
            "product_name": "Nama Produk",
            "product_price": "Harga (RM)",
            "product_category_name": "Kategori",
            "product_description": "Deskripsi",
        }
    def clean_product_name(self):
        name = self.cleaned_data.get('product_name')
        if not name:
            raise ValidationError("Product name is required.")
        return name

    def clean_product_description(self):
        desc = self.cleaned_data.get('product_description')
        if desc:
            word_count = len(desc.split())
            if word_count < 3:
                raise ValidationError("Product description must be at least 3 words.")
        return desc

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("no_variant"):          # kes tiada varian
            if cleaned.get("product_price") is None:
                self.add_error("product_price", "Sila masukkan harga.")
            if cleaned.get("base_quantity") is None:
                self.add_error("base_quantity", "Sila masukkan stok.")
        return cleaned


class VariantForm(ModelForm):
    class Meta:
        model   = ProductVariant
        exclude = ("product",)
        widgets = {
            "variant_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Variant (e.g. 500 g)"}),
            "variant_price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}),
            "variant_quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}),
        }

VariantFormSet = inlineformset_factory(
    parent_model   = Product,
    model          = ProductVariant,
    form           = VariantForm,
    extra          = 0,      # show one empty row
    can_delete     = True,
    min_num        = 1,      # at least one variant
    validate_min   = False,
)


