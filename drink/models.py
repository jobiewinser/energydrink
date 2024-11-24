import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_countries.fields import CountryField
from core.models import CURRENCIES, CONTAINER_TYPES
from django.db.models import Avg
import math


def save_average_drink_reviews(drink):
    avrg_taste = drink.review_drink.aggregate(Avg("taste"))["taste__avg"]
    drink.average_taste = round(avrg_taste if avrg_taste is not None else 0, 0)

    drink.save(calculate_average_reviews=False)


class Brand(models.Model):
    name = models.TextField(null=False)
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="brand_submitted_by",
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="brand_approved_by",
    )
    approved = models.BooleanField(default=False, blank=True)


def drink_file_name(instance, filename):
    filename = "%s_%s" % (instance.id, filename)
    return os.path.join("drinks", filename)


class Container(models.Model):
    CONTAINER_TYPE_CHOICES = CONTAINER_TYPES
    container_type = models.CharField(choices=CONTAINER_TYPE_CHOICES, blank=True, null=True)
    size = models.IntegerField(
        null=True,
        blank=True,
    )


class Drink(models.Model):
    name = models.TextField(null=False)
    brand = models.ForeignKey(
        "drink.Brand",
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
    image = models.ImageField(default="default.png", upload_to=drink_file_name)
    average_taste = models.IntegerField(null=False, blank=True, default=0)
    caffeine_per_hundred_ml = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )
    calories_per_hundred_ml = models.IntegerField(
        null=True,
        blank=True,
    )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        calculate_average_reviews=True,
    ):
        super(Drink, self).save(force_insert, force_update, using, update_fields)
        if calculate_average_reviews:
            save_average_drink_reviews(self)


class Review(models.Model):
    REVIEW_CURRENCIES = CURRENCIES
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
    country_purchased = CountryField(
        blank_label="(select country)", blank=True, null=True
    )
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
    currency = models.CharField(choices=REVIEW_CURRENCIES, blank=True, null=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Review, self).save(force_insert, force_update, using, update_fields)
        drink = self.drink
        if drink:
            save_average_drink_reviews(drink)
