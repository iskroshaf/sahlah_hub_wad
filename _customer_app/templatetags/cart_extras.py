from django import template
register = template.Library()

@register.filter
def get_item(d, k):
    return d.get(k, 0)

@register.filter
def subtract(value, arg):
    
    try:
        return value - arg
    except Exception:
        return value