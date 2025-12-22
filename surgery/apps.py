from django.apps import AppConfig


class SurgeryConfig(AppConfig):
    name = 'surgery'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import surgery.signals