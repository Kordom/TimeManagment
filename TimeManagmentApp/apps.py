from django.apps import AppConfig


class TimemanagmentappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "TimeManagmentApp"

    def ready(self):
        from .signals import create_profile