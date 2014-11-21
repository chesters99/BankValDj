from time import sleep
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth import user_login_failed
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(user_login_failed)
def delay_next_login(sender, credentials, **kwargs):
    sleep(1)
