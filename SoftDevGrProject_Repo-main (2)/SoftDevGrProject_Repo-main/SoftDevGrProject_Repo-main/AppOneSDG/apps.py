from django.apps import AppConfig
import sys


class ApponesdgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppOneSDG'
    def ready(self):
    # Prevent scheduler from running during migrations
     if "runserver" in sys.argv:
        from . import scheduler
        scheduler.start()
