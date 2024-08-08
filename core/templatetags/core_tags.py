import os
from django import template
from datetime import datetime, timedelta
import time
import calendar
import uuid

from django.conf import settings

register = template.Library()
from django.contrib.auth.models import User
import math


@register.filter
def range_tag(range_lower, range_upper):
    if (type(range_lower), type(range_upper)) == (int, int):
        if range_lower < range_upper:
            result = range(range_lower, range_upper)
            return result
    return []


@register.filter
def round_tag(number, digits):
    return round(float(number), int(digits))


@register.filter
def str_tag(var):
    return str(var)
