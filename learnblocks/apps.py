from .utils.s3 import connect_s3
from django.apps import AppConfig


class LearnblocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learnblocks'

    def ready(self):
        import learnblocks.signals
        connect_s3()
