from django.contrib import admin
from core.models import *
from django.apps import apps

models = apps.get_models()

# Register your models here.


for model in models:
    try:
        admin.site.register(model)  # Register all models that aren't already registered
    except:
        pass  # If the model is already registed, don't bother
