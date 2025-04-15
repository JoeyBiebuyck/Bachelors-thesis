from django import template

register = template.Library()

@register.filter()
def basic_filter(input):
    pass