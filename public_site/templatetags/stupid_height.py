from django import template
register = template.Library()

@register.filter
def stupid_height(list):
    return len(list)*14 + 5
