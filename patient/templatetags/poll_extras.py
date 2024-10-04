from datetime import timedelta

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


@register.filter(name='calculate_appointment_date')
def calculate_appointment_date(appointment_date, duration):
    result = appointment_date + timedelta(minutes=duration)
    print(result)
    return result


@register.filter(name='remove_lang')
def calculate_appointment_date(url):
    url_without_lang = "/".join(url.split("/")[0:3])
    print(url_without_lang)
    return url_without_lang
