from django.conf import settings

# Define language name translations
LANGUAGE_NAMES = {
    'en': {'en': 'English', 'ms': 'Malay', 'ar': 'Arabic'},
    'ms': {'en': 'Bahasa Inggeris', 'ms': 'Bahasa Melayu', 'ar': 'Bahasa Arab'},
    'ar': {'en': 'الإنجليزية', 'ms': 'الملايو', 'ar': 'العربية'}
}

def global_settings(request):
    current_language = request.LANGUAGE_CODE  # Get the active language

    languages = []
    for lang in settings.PARLER_LANGUAGES[None]:
        code = lang['code']
        name = LANGUAGE_NAMES.get(current_language, {}).get(code, lang['name'])
        languages.append((code, name))

    return {
        'SITE_NAME': 'Sahlan Hub',
        'SUPPORT_EMAIL': 'support@sahlanhub.com',
        'languages': languages,
    }
