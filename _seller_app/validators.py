import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_("Password mesti sekurang-kurangnya 8 aksara."))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password mesti mengandungi sekurang-kurangnya satu huruf kecil (a-z)."))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password mesti mengandungi sekurang-kurangnya satu huruf besar (A-Z)."))
        if not re.search(r'\d', password):
            raise ValidationError(_("Password mesti mengandungi sekurang-kurangnya satu nombor (0-9)."))
       
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(_("Password mesti mengandungi sekurang-kurangnya satu aksara khas (contoh: !@#$%)."))

    def get_help_text(self):
        return _(
            "Password anda mesti memenuhi kesemua:\n"
            "• 8 aksara atau lebih\n"
            "• Sekurang-kurangnya satu huruf kecil (a-z)\n"
            "• Sekurang-kurangnya satu huruf besar (A-Z)\n"
            "• Sekurang-kurangnya satu nombor (0-9)\n"
            "• Sekurang-kurangnya satu aksara khas (contoh: !@#$%)"
        )
