from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_countries.fields import CountryField
from core.models import CURRENCY_CHOICES
from django.db.models import Avg
import math

def save_average_drink_reviews(drink):    
    avrg_taste = drink.review_drink.aggregate(Avg("taste"))["taste__avg"]
    drink.average_taste = round(avrg_taste if avrg_taste is not None else 0, 0)

    avrg_aftertaste = drink.review_drink.aggregate(Avg("aftertaste"))["aftertaste__avg"]
    drink.average_aftertaste = round(avrg_aftertaste if avrg_aftertaste is not None else 0, 0)
    drink.save(calculate_average_reviews=False)

class DrinkBrand(models.Model):
    name = models.TextField(null=False)
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_brand_submitted_by",
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_brand_approved_by",
    )
    approved = models.BooleanField(default=False, blank=True)


class Drink(models.Model):
    name = models.TextField(null=False)
    drink_brand = models.ForeignKey(
        "drink.DrinkBrand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved = models.BooleanField(default=False, blank=True)
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_submitted_by",
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_approved_by",
    )
    image = models.ImageField(default="default.png", upload_to="drinks")
    average_taste = models.IntegerField(null=False, blank=True, default=0)
    average_aftertaste = models.IntegerField(null=False, blank=True, default=0)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, calculate_average_reviews=True
    ):
        super(Drink, self).save(force_insert, force_update, using, update_fields)
        if calculate_average_reviews:
            save_average_drink_reviews(self)


class Review(models.Model):
    REVIEW_CURRENCY_CHOICES = CURRENCY_CHOICES
    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_submitted_by",
    )
    taste = models.IntegerField(null=False, blank=True, default=0)
    aftertaste = models.IntegerField(null=False, blank=True, default=0)
    title = models.TextField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    drink = models.ForeignKey(
        "drink.Drink",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_drink",
    )
    image = models.ImageField(default="default.png", upload_to="reviews")
    country_purchased = CountryField(blank_label="(select country)", blank=True, null=True)
    # city_purchased = models.ForeignKey(
    #     "core.Country",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    price_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    currency = models.CharField(choices=REVIEW_CURRENCY_CHOICES, blank=True, null=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Review, self).save(force_insert, force_update, using, update_fields)
        drink = self.drink
        if drink:
            save_average_drink_reviews(drink)