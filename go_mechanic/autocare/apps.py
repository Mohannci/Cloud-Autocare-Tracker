from django.apps import AppConfig


class AutocareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'go_mechanic.autocare'  # Must match the full module path
    label = 'autocare'