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
def stars(rating):
    full_stars = int(rating)
    half_star = rating - full_stars
    return {"full_stars": full_stars, "half_star": half_star > 0.5}
