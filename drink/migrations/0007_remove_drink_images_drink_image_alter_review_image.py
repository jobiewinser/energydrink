# Generated by Django 5.0.1 on 2024-07-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drink", "0006_remove_review_images_review_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="drink",
            name="images",
        ),
        migrations.AddField(
            model_name="drink",
            name="image",
            field=models.ImageField(default="default.png", upload_to="drinks"),
        ),
        migrations.AlterField(
            model_name="review",
            name="image",
            field=models.ImageField(default="default.png", upload_to="reviews"),
        ),
    ]