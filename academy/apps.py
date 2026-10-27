from django.apps import AppConfig


class AcademyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "academy"

    # Preserve the existing database table and migration labels.
    label = "mousey"
