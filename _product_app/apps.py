from django.apps import AppConfig


class ProductAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '_product_app'

    def ready(self):
        import _product_app.signals
