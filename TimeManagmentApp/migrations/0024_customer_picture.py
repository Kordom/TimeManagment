# Generated by Django 5.0.6 on 2024-06-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0023_project_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="picture",
            field=models.ImageField(
                blank=True, default="no-image.png", upload_to="customer_pics"
            ),
        ),
    ]
