from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

# you change change the name here
app = Celery('core')

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

## Periodic task schedule!! ##
app.conf.beat_schedule = {
    'inactivate-dormant-users': {
        'task': 'inactivate_dormant_users',
        'schedule': crontab(minute=0, hour=3),
        'args': (26,)
    },
    'delete_old_sequences': {
        'task': 'delete_old_sequences',
        'schedule': crontab(minute=30, hour=3),
        'args': (14,)
    }
}
