from __future__ import absolute_import
from celery import shared_task
import time


@shared_task
def test_task(param=2):
    time.sleep(param)
    return 'yes!!! task completed sleeping for %i seconds!' % param

