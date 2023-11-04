import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from core.parser import parse_data
            parse_data()
        else: pass