import httplib2
from os import path
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from eventlog.models import log
from BankValDj.middleware import get_current_user
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import transaction


def logged_in_message(user, request, **kwargs):
    """Add a welcome message when the user logs in """
    messages.success(request, "User '%s' successfully logged in" % user.username)

user_logged_in.connect(logged_in_message)

def weight_validator(weight):
    if not (-255 <= weight <= 255):
        raise ValidationError("Weight is -255 to 255")

class SmallIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if 'mysql' in connection.settings_dict['ENGINE']:
            return "smallint"
        else:
            return super(SmallIntegerField, self).db_type(connection)


class CommonModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', editable=False)
    active = models.BooleanField(default=True)
    site = models.ForeignKey(Site, editable=False)

    class Meta:
        abstract = True


class Rule(CommonModel):
    MODULUS_10 = 'MOD10'
    MODULUS_11 = 'MOD11'
    DOUBLE_ALT = 'DBLAL'
    RULE_CHOICE = ((MODULUS_10, MODULUS_10), (MODULUS_11, MODULUS_11), (DOUBLE_ALT, DOUBLE_ALT))

    start_sort = models.CharField(max_length=6, db_index=True, help_text=_('from this sort code'))
    end_sort = models.CharField(max_length=6, db_index=True, help_text=_('to this sort code'))
    mod_rule = models.CharField(max_length=255, choices=RULE_CHOICE, help_text=_('determine which algorithm to apply'))
    mod_exception = models.CharField(max_length=2, blank=True, help_text=_('exception rule'))
    weight = ArrayField(models.SmallIntegerField(validators=[weight_validator]), size=14, verbose_name='Weights')
    # objects manager accesses all records, site manager access only records for the current site
    objects = models.Manager()
    current = CurrentSiteManager('site')

    class Meta:
        ordering = ['id', ]
        # index_together = [ ["start_sort", "end_sort"], ] # doesnt offer a performance advantage

    def __str__(self):
        return '%s %s-%s' % (self.id, self.start_sort, self.end_sort)

    def delete(self, using=None, keep_parents=None):  # turn physical delete requests into logical deletes
        if self.active:
            self.active = False
            self.save()
        else:
            super(Rule, self).delete()

    def save(self, *args, **kwargs):
        if not hasattr(self, 'site'):
            self.site = Site.objects.get_current()
        user = get_current_user()
        user_model = get_user_model()
        if not isinstance(user, user_model):
            user = user_model.objects.first()  # if no user available then assume 1st user is superuser
        self.updated_by = user
        if not self.pk:
            self.created_by = user
            log(user=user, action='ADD_RULE', extra={'id': self.id, 'start_sort': self.start_sort})
        else:
            log(user=user, action='UPDATE_RULE', extra={'id': 0, 'start_sort': self.start_sort})
        return super(Rule, self).save(*args, **kwargs)

    def get_absolute_url(self):  # this is not working so not used - gets a NoReverseMatch exception
        return reverse('rules:detail', kwargs={'pk': self.id})


def load_rules(filename: str, sort_code=None):
    if 'https:' in filename:
        response, content = httplib2.Http('.cache').request(filename)
        if response.status not in (200, 301):
            raise RuntimeError('%s %s' % (response.status, response.reason))
        f = content.decode("utf-8").split('\r\n')
    else:
        filename = path.join(settings.MEDIA_ROOT, filename).replace('..', '')
        f = open(filename, "r")
    with transaction.atomic():
        Rule.objects.all().delete(); Rule.objects.all().delete() # once to inactivate, then to delete inactive
        for counter, line in enumerate(f):
            if line and line[0:5] <= (sort_code or line[0:5]) <= line[7:12]:
                items = [item for item in line.strip().split()]
                try:
                    mod_exception = items[17]
                except IndexError:
                    mod_exception = ''
                Rule.objects.create(start_sort=items[0], end_sort=items[1], mod_rule=items[2],
                                    weight=[items[w] for w in range(3,17)], mod_exception=mod_exception )
    return counter
