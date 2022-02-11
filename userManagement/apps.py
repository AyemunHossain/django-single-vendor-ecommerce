from django.apps import AppConfig

class UsermanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userManagement'

    def ready(self):
        import userManagement.signals