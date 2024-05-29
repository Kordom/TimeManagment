# Generated by Django 5.0.6 on 2024-05-25 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0007_task_project"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="worker",
            name="tasks",
        ),
        migrations.AddField(
            model_name="task",
            name="worker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="TimeManagmentApp.worker",
            ),
        ),
    ]
