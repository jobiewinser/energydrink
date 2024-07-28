from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


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
    approved = models.BooleanField(default=False)


class Drink(models.Model):
    name = models.TextField(null=False)
    drink_brand = models.ForeignKey(
        "drink.DrinkBrand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved = models.BooleanField(default=False)
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


class Review(models.Model):
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
    title = models.TextField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    # approved = models.BooleanField(default=False)
    drink = models.ForeignKey(
        "drink.Drink",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_drink",
    )
    # approved_by = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #
    #     null=True,
    #     related_name="drink_approved_by",
    # )
    # images = ArrayField(
    #     models.ImageField(default="default.png", upload_to="drinks"),
    #     null=True,
    #     blank=True,
    #     default=list,
    # )
    image = models.ImageField(default="default.png", upload_to="reviews")
    city_purchased = models.ForeignKey(
        "core.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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
    # images = models.ImageField(default='default.png', upload_to='profile_images')
    # created = models.DateTimeField(auto_now_add=True, null=True)
    # REQUEST_TYPE_CHOICES = (
    #                     ('a', 'POST'),
    #                     ('b', 'GET'),
    #                 )
    # json_data = models.JSONField(null=True)
    # meta_data = models.JSONField(default=dict)
    # errors = models.ManyToManyField("core.ErrorModel", null=True)
    # request_type = models.CharField(choices=REQUEST_TYPE_CHOICES, default='a', max_length=1)
