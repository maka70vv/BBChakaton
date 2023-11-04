import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from core.parser import parse_data
            from core.contractsParser import parse_data2

            parse_data()
            parse_data2()
        else: pass