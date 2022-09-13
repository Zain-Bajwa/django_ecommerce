"""Filters for django templates"""

from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    """Returns the list of1 to number"""
    return range(int(number))
