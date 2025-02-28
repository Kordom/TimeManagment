# Generated by Django 5.0.6 on 2024-05-31 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "TimeManagmentApp",
            "0021_remove_project_created_at_remove_project_updated_at_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="availability_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Available From"
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="status",
            field=models.CharField(
                choices=[("ISA", "Available"), ("NOT", "Not Available")],
                default="NOT",
                help_text="Worker availability status",
                max_length=3,
            ),
        ),
    ]
