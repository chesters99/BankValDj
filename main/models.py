from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from eventlog.models import log
from pytz import all_timezones
from .countries import COUNTRIES
from django.conf import settings
from django.contrib.auth.models import User

TIME_ZONE_CHOICES = [(tz, tz) for tz in all_timezones]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    time_zone = models.CharField(max_length=50, blank=False, default=settings.TIME_ZONE, choices=TIME_ZONE_CHOICES)
    address_line1 = models.CharField(max_length=50, blank=True)
    address_line2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    post_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=40, blank=False, choices=COUNTRIES, default='GB')
    stripe_customer_id = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return '%s %s' % (self.user_id, self.country)

    def save(self, *args, **kwargs):
        self.time_zone = timezone.get_current_timezone_name()
        if not self.pk:
            log(user=self.user, action='ADD_USERP', extra={'id': self.id, 'user_name': self.user.username})
        else:
            log(user=self.user, action='UPD_USERP', extra={'id': 0, 'user_name': self.user.username})
        return super(UserProfile, self).save(*args, **kwargs)
