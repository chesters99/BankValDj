from time import sleep
from django.contrib.auth import user_login_failed
from django.dispatch import receiver


@receiver(user_login_failed)
def delay_next_login(sender, credentials, **kwargs):
    sleep(3)
