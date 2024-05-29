# Generated by Django 5.0.6 on 2024-05-25 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "TimeManagmentApp",
            "0012_worker_price_per_hour_alter_vehicle_project_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="place_city",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="City"
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Project name"),
        ),
    ]
