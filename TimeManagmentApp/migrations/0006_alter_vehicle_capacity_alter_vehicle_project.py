# Generated by Django 5.0.6 on 2024-05-25 09:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0005_alter_vehicle_capacity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="capacity",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(8),
                    django.core.validators.MinValueValidator(1),
                ],
                verbose_name="Capacity (1-8)",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="TimeManagmentApp.project",
            ),
        ),
    ]
