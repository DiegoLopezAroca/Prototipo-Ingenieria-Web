from django.apps import AppConfig


class AppprojectdjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appProjectDjango'
    
    def ready(self):
            import appProjectDjango.signals  # importa los signals