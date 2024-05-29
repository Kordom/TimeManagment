# Generated by Django 5.0.6 on 2024-05-25 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0011_remove_vehicle_workers_worker_vehicle"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="price_per_hour",
            field=models.FloatField(default=0, verbose_name="Price per hour"),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="TimeManagmentApp.project",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="vehicle",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="TimeManagmentApp.vehicle",
            ),
        ),
    ]
