from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class Profile(models.Model):
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(default="default.png", upload_to="profile_images")
    theme = models.CharField(max_length=10, default="light")
