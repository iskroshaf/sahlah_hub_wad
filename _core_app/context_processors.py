from django.conf import settings

def global_settings(request):
    return {
        'SITE_NAME': 'Sahlan Hub',
        'SUPPORT_EMAIL': 'support@sahlanhub.com',
        "languages": settings.LANGUAGES, 
    }

