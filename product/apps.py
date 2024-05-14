from django.apps import AppConfig

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        # Import signal handlers when the app is ready
         from . import signals