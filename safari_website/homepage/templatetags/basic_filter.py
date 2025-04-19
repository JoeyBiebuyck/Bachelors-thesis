from django import template

register = template.Library()

@register.filter()
def basic_filter(input):
    allowed_inputs = []
    if input in allowed_inputs:
        return 1
    else:
        return 0