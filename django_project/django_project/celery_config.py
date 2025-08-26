from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')

# Load config from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_finalize.connect
def run_once(sender, **kwargs):
    from api.rag_background.tasks import add
    sender.send_task('api.rag_background.tasks.add', args=[3, 5])
