from django import template
register = template.Library()
@register.filter
def split(value, separator=','):
    return [x.strip() for x in str(value or '').split(separator) if x.strip()]
