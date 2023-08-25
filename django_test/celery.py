import os
import django
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
django.setup()
app = Celery("django_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update()
app.autodiscover_tasks(['django_test.tasks'])