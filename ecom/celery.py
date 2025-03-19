import os
from celery import Celery

# set django default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

app = Celery('ecom')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover all tasks in Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')