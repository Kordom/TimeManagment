# Generated by Django 5.0.6 on 2024-05-25 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0009_vehicle_workers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vehicle",
            name="workers",
        ),
        migrations.AddField(
            model_name="vehicle",
            name="workers",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="TimeManagmentApp.worker",
            ),
        ),
    ]
