from django.apps import AppConfig


class AppConfig(AppConfig):
    """ Esta clase es la base para la configuración de la aplicación
    de Django "app"."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
