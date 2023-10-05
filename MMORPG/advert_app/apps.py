from django.apps import AppConfig


class AdvertAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advert_app'

    def ready(self):
        __import__(name='advert_app', fromlist=['signals'])
