import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'go_mechanic.backend.settings')

application = get_wsgi_application()