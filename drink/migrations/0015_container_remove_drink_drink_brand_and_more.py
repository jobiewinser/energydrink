# Generated by Django 5.0.1 on 2024-11-10 15:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drink", "0014_remove_drink_average_aftertaste_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Container",
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
                (
                    "container_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("can", "Can"),
                            ("bottle", "Bottle"),
                            ("carton", "Carton"),
                        ],
                        null=True,
                    ),
                ),
                ("size", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name="drink",
            old_name="drink_brand",
            new_name="brand",
        ),
        migrations.AddField(
            model_name="drink",
            name="calories_per_hundred_ml",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RenameModel(
            old_name = "DrinkBrand",
            new_name = "Brand",
        ),
    ]