from google.cloud import translate_v2 as translate
from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from _core_app.utils import generate_unique_id

def detect_language(text):
    """Detect language using Google Cloud Translation API with restricted choices."""
    if not text:
        return "en"  # Default to English if empty
    
    client = translate.Client()
    result = client.detect_language(text)
    
    detected_lang = result.get("language", "en")  # Default to English if detection fails
    
    # Force detection to only consider 'en', 'ms', and 'ar'
    if detected_lang not in ['en', 'ms', 'ar']:
        detected_lang = "en"  # Default fallback
        print('Undetect',detected_lang)
    return detected_lang



def translate_text(text, target_language):
    """Translate text using Google Cloud Translation API."""
    if not text:
        return ""
    
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

class BaseTranslatableModel(TranslatableModel):
    """Base model for automatic translation into multiple languages."""

    def auto_translate(self, fields):
        """Automatically translates specified fields into target languages."""
        translations = {}
        detected_lang = 'en'
        
        for field in fields:
            original_text = getattr(self, field, "")
            if original_text:
                detected_lang = detect_language(original_text)  # Detect language using Google API
                break  # Detect once from any non-empty field
        
        if detected_lang == 'en':
            source_language = 'en'
            target_languages = ['ms', 'ar']
        elif detected_lang == 'ms':
            source_language = 'ms'
            target_languages = ['en', 'ar']
        elif detected_lang == 'ar':
            source_language = 'ar'
            target_languages = ['en', 'ms']
        else:
            source_language = 'en'
            target_languages = ['ms', 'ar']
        
        translations[source_language] = {}
        for field in fields:
            translations[source_language][field] = getattr(self, field, "")
        
        for lang in target_languages:
            translations[lang] = {}
            for field in fields:
                translated_text = translate_text(translations[source_language][field], lang)
                translations[lang][field] = translated_text
        
        super().save()  # Save the instance first
        
        # Save translations
        for lang, translated_fields in translations.items():
            self.set_current_language(lang)
            for field, translated_value in translated_fields.items():
                setattr(self, field, translated_value)
            super().save()

        self.set_current_language('en')  # Reset to default language

    class Meta:
        abstract = True  # Make this an abstract model

class Product(BaseTranslatableModel):
    shop = models.ForeignKey('_shop_app.Shop', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=10, unique=True, primary_key=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_category_name = models.ForeignKey('_product_app.ProductCategory', on_delete=models.SET_NULL, null=True, blank=True)
    translations = TranslatedFields(
        product_name=models.CharField(max_length=50),
        product_description=models.TextField(max_length=250, blank=True, null=True),
    )

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_unique_id(Product, 'prd', 'product_id')

        is_new = self._state.adding  # Check if it's a new instance
        super().save(*args, **kwargs)

        if is_new:
            self.auto_translate(fields=['product_name', 'product_description'])

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product"

class ProductCategory(BaseTranslatableModel):
    translations = TranslatedFields(
        product_category_name=models.CharField(max_length=25),
    )
    shop = models.ForeignKey('_shop_app.Shop', on_delete=models.CASCADE)
    product_category_id = models.CharField(max_length=10, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.product_category_id:
            self.product_category_id = generate_unique_id(ProductCategory, 'pcg', 'product_category_id')
            
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.auto_translate(fields=['product_category_name'])

    def __str__(self):
        return self.product_category_name

    class Meta:
        db_table = "product_category"
