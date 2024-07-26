import base64
import json
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import bleach
from django.db.models import JSONField

from messaging.models import Message, MessageImage
from django.dispatch import receiver
from PIL import Image
from io import StringIO, BytesIO
            
from datetime import datetime, timedelta
from django.core.files.images import ImageFile
import os

GYM_CHOICES = (
                    ('a', 'Abingdon'),
                    ('b', 'Alton'),
                    ('c', 'Fleet')
                )

class DrinkBrand(models.Model):
    name = models.TextField(null=False, blank=False)
    
class Drink(models.Model):
    name = models.TextField(null=False, blank=False)
    drink_brand = models.ForeignKey('drink.DrinkBrand', on_delete=models.SET_NULL, null=True, blank=True)
    # created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # REQUEST_TYPE_CHOICES = (
    #                     ('a', 'POST'),
    #                     ('b', 'GET'),
    #                 )
    # json_data = models.JSONField(null=True, blank=True)
    # meta_data = models.JSONField(default=dict)
    # errors = models.ManyToManyField("core.ErrorModel", null=True, blank=True)
    # request_type = models.CharField(choices=REQUEST_TYPE_CHOICES, default='a', max_length=1)