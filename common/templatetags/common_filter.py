from django import template

register = template.Library()


@register.filter
def abridge(value, arg):
    return value[:arg]


@register.filter
def length(value):
    return len(value)

@register.filter
def count(value):
    return value.length
