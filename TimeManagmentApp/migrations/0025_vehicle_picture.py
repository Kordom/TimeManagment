# Generated by Django 5.0.6 on 2024-06-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0024_customer_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="picture",
            field=models.ImageField(
                blank=True, default="no-image.png", upload_to="vehicle_pics"
            ),
        ),
    ]
