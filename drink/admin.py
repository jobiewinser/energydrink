from django.contrib import admin
from drink.models import *

# Register your models here.


class DrinkBrandAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "approved"]
    search_fields = ["pk", "name", "approved"]


admin.site.register(DrinkBrand, DrinkBrandAdmin)
