from django.http import HttpResponse
from django.apps import AppConfig
import os
class Myappconfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parser'
    a = 0

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from parser.parser import parse_data
            parse_data()
        else: pass
