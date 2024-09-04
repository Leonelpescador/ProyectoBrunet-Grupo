from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'

from django.apps import AppConfig

class RestaurantConfig(AppConfig):
    name = 'restaurant'

    def ready(self):
        import restaurant.signals