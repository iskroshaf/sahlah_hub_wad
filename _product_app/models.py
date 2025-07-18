from google.cloud import translate_v2 as translate
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from _core_app.utils import generate_unique_id
from django.utils.translation import get_language
from django.dispatch import receiver


def translate_text(text, target_language):
    if not text:
        return ""

    client = translate.Client()
    detected_language = client.detect_language(text)["language"]

    current_language = get_language()
    if current_language == "en" and detected_language == "en":
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    elif current_language == "ms" and detected_language == "ms":
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    elif current_language == "ar" and detected_language == "ar":
        result = client.translate(text, target_language=target_language)
        return result["translatedText"]
    return text


class BaseTranslatableModel(TranslatableModel):
    """Base model for automatic translation into multiple languages."""

    def auto_translate(self, fields):
        """Automatically translates specified fields based on the current language."""
        current_language = get_language()
        target_languages = []

        if current_language == "en":
            for field in fields:
                original_text = getattr(self, field)
                detected_language = translate.Client().detect_language(original_text)[
                    "language"
                ]

                if detected_language != "en":
                    self.set_current_language("en")
                    setattr(self, field, original_text)
                    continue  # Skip translation to other languages

                target_languages = ["ms", "ar"]  # Translate English to Malay and Arabic
        elif current_language == "ms":
            for field in fields:
                original_text = getattr(self, field)
                detected_language = translate.Client().detect_language(original_text)[
                    "language"
                ]

                if detected_language != "ms":
                    self.set_current_language("ms")
                    setattr(self, field, original_text)
                    continue  # Skip translation to other languages

                target_languages = ["en", "ar"]  # Translate English to Malay and Arabic
        elif current_language == "ar":
            for field in fields:
                original_text = getattr(self, field)
                detected_language = translate.Client().detect_language(original_text)[
                    "language"
                ]

                if detected_language != "ar":
                    self.set_current_language("ar")
                    setattr(self, field, original_text)
                    continue  # Skip translation to other languages

                target_languages = ["ms", "ar"]  # Translate English to Malay and Arabic
        else:
            return  # No translation for other languages

        for field in fields:
            original_text = getattr(self, field)
            for lang_code in target_languages:
                translated_text = translate_text(original_text, lang_code)
                self.set_current_language(lang_code)
                setattr(self, field, translated_text)

        self.set_current_language(current_language)  # Reset to original language
        self.save()

    class Meta:
        abstract = True  # Make this an abstract model


class Product(BaseTranslatableModel):

    PRODUCT_STATUS_CHOICES = [
    ('available',     'Available'),
    ('non-available', 'Non-Available'),
    ]
    
    shop = models.ForeignKey("_shop_app.Shop", on_delete=models.CASCADE)
    product_id = models.CharField(max_length=10, unique=True, primary_key=True)
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,    # ijinkan NULL
        blank=True,   # optional untuk form
    )
    product_quantity = models.PositiveIntegerField(
        default=0,
        editable=False,     # tak boleh diisi manual
        help_text="Jumlah stok semua varian"
    )
    # product_image = models.ImageField(upload_to='media_photos/', blank=True, null=True)
    product_category_name = models.ForeignKey(
        "_product_app.ProductCategory", on_delete=models.SET_NULL, null=True, blank=True
    )

    translations = TranslatedFields(
        product_name=models.CharField(max_length=50),
        product_description=models.TextField(max_length=250, blank=True, null=True),
    )

    product_availability = models.CharField(
        max_length=15,
        choices=PRODUCT_STATUS_CHOICES,
        default='available',
    )

    no_variant = models.BooleanField(default=True)
    
    #Implement model Halal_Haram
    HALAL_STATUS_CHOICES =[
        ("Halal","Halal"),
        ("Haram","Haram"),
        ("Mashbooh","Mashbooh"),
        ("Unknown","Unknown"),
    ]
    
    halal_status=models.CharField(max_length=10,choices=HALAL_STATUS_CHOICES,default="Unknown")
    #Implement model Halal_Haram
    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_unique_id(Product, "prd", "product_id")
            

        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.auto_translate(fields=["product_name", "product_description"])

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product"


class ProductCategory(BaseTranslatableModel):
    translations = TranslatedFields(
        product_category_name=models.CharField(max_length=25),
    )
    
    product_category_id = models.CharField(max_length=10, unique=True, primary_key=True)
    def save(self, *args, **kwargs):
        if not self.product_category_id:
            self.product_category_id = generate_unique_id(
                ProductCategory, "pcg", "product_category_id"
            )

        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.auto_translate(fields=["product_category_name"])

    def __str__(self):
        return self.product_category_name

    class Meta:
        db_table = "product_category"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        db_table = "product_images"

    def __str__(self):
        return f"Image for {self.product.product_name}"

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants'
    )
    variant_name     = models.CharField(max_length=50)
    variant_price    = models.DecimalField(max_digits=10, decimal_places=2)
    variant_quantity = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_name} – {self.variant_name}"

    class Meta:
            db_table = "product_variant"