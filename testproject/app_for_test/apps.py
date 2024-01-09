from django.apps import AppConfig


class AppForTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_for_test'
