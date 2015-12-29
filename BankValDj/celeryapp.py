from __future__ import absolute_import
import os
import django
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BankValDj.settings.local')
django.setup()

app = Celery('BankValDj')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.LOCAL_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# startup for redis, celery on local
# redis-server /usr/local/etc/redis.conf
# celery -A BankValDj worker -B --loglevel=INFO --concurrency=4
# redis-cli <cr> shutdown <cr> exit <cr>
