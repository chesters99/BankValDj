from __future__ import absolute_import
import django
from celery import Celery
from django.conf import settings

django.setup()
app = Celery('BankValDj')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.LOCAL_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# startup for redis, celery on local
# redis-server /usr/local/etc/redis.conf
# celery -A BankValDj worker -B --loglevel=INFO --concurrency=4
# redis-cli <cr> shutdown <cr> exit <cr>
