import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'univer.settings')
app = Celery('univer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()