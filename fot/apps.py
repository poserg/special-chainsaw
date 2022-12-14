from django.apps import AppConfig


class FotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fot'

    def ready(self):
        import fot.signals.handlers # noqa
