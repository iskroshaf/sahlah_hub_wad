from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from google.cloud import translate_v2 as translate

class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        description=models.TextField(),
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Automatically translate and save translations for 'ar' and 'ms'."""
        if not self.id:  # Only translate when creating a new product
            client = translate.Client()
            translations = {}

            for lang_code in ['ar', 'ms']:
                translations[lang_code] = {
                    "name": client.translate(self.name, target_language=lang_code)["translatedText"],
                    "description": client.translate(self.description, target_language=lang_code)["translatedText"],
                }

            super().save(*args, **kwargs)  # Save the product first

            for lang_code, trans in translations.items():
                self.set_current_language(lang_code)
                self.name = trans["name"]
                self.description = trans["description"]
                super().save()  # Save translations

            self.set_current_language('en')  # Reset back to English

        else:
            super().save(*args, **kwargs)  # Normal save for updates

    class Meta:
        db_table = "product"
