from django.apps import AppConfig


class ObgynConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obgyn_config'

    def ready(self) -> None:
        import obgyn_config.signals