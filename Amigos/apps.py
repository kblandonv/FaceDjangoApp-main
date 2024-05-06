from django.apps import AppConfig


class AmigosConfig(AppConfig):
    """
    AppConfig for the 'Amigos' app.

    This class represents the configuration for the 'Amigos' app in Django.
    It sets the default auto field to 'django.db.models.BigAutoField' and
    specifies the name of the app as 'Amigos'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Amigos'
