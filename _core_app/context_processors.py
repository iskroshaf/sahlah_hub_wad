from django.conf import settings
from django.utils.translation import gettext_lazy as _

LANGUAGE_NAMES = {
    'en': {'en': _('English'), 'ms': _('Malay'), 'ar': _('Arabic')},
    'ms': {'en': _('Bahasa Inggeris'), 'ms': _('Bahasa Melayu'), 'ar': _('Bahasa Arab')},
    'ar': {'en': _('الإنجليزية'), 'ms': _('الملايو'), 'ar': _('العربية')}
}

def global_settings(request):
    current_language = request.LANGUAGE_CODE
    languages = [
        (lang['code'], LANGUAGE_NAMES.get(current_language, {}).get(lang['code'], _(lang['name'])))
        for lang in settings.PARLER_LANGUAGES.get(None, [])
    ]

    return {
        'SITE_NAME': 'Sahlan Hub',
        'SUPPORT_EMAIL': 'support@sahlanhub.com',
        'languages': languages,
    }
