# _core_app/templatetags/math_filters.py
from django import template
register = template.Library()
@register.filter
def mul(value, arg):
    """
    Darab dua nombor: {{ a|mul:b }} → a * b
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
