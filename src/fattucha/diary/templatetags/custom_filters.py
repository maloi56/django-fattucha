from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def minus(value, arg):
    return int(value) - int(arg)


@register.filter
def plus(value, arg):
    return int(value) + int(arg)


@register.filter
def to_str(value):
    return str(value)


@register.filter
def delta_minus(arg, value):
    try:
        return datetime.strptime(arg, "%Y-%m-%d").date() - timedelta(hours=value)
    except TypeError:
        return ''


@register.filter
def delta_sum(arg, value):
    try:
        return datetime.strptime(arg, "%Y-%m-%d").date() + timedelta(hours=value)
    except TypeError:
        return ''


@register.filter
def get_week_period(week, year):
    first_day_of_week = datetime.strptime(f'{year}-{week}-1', "%Y-%W-%w").date()
    result = f'{first_day_of_week} - {first_day_of_week + timedelta(6)}'
    return result
