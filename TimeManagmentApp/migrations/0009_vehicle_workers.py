# Generated by Django 5.0.6 on 2024-05-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TimeManagmentApp", "0008_remove_worker_tasks_task_worker"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="workers",
            field=models.ManyToManyField(to="TimeManagmentApp.worker"),
        ),
    ]
