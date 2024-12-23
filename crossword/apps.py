from django.apps import AppConfig


class CrosswordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crossword'

    def ready(self):
        from .utils import generate_crossword_data
