import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "univer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from .celery import app as celery_app
__all__ = ('celery_app',)