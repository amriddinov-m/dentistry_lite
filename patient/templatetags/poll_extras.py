from django import template

register = template.Library()





@register.filter(name='remove_zero')
def remove_zero(val):
    try:
        return int(val)
    except ValueError:
        val = val.split(',')[0]
        val = val.split('.')[0]
        return val
