# Generated by Django 5.0.1 on 2024-07-28 10:56

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_city_country_alter_profile_avatar_alter_profile_user_and_more"),
        ("drink", "0002_drink_approved_drink_approved_by_drink_submitted_by_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="drink",
            name="images",
            field=models.ImageField(default="default.png", upload_to="profile_images"),
        ),
        migrations.AlterField(
            model_name="drink",
            name="approved_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="drink_approved_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="drink",
            name="drink_brand",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="drink.drinkbrand",
            ),
        ),
        migrations.AlterField(
            model_name="drink",
            name="submitted_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="drink_submitted_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="drinkbrand",
            name="approved_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="drink_brand_approved_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="drinkbrand",
            name="submitted_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="drink_brand_submitted_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("title", models.TextField(null=True)),
                ("description", models.TextField(null=True)),
                (
                    "images",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.ImageField(
                            default="default.png", upload_to="profile_images"
                        ),
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "price_paid",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                ("currency", models.CharField(max_length=10, null=True)),
                (
                    "city_purchased",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.city",
                    ),
                ),
                (
                    "drink",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="review_drink",
                        to="drink.drink",
                    ),
                ),
                (
                    "submitted_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="review_submitted_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]