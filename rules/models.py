import httplib2
from django.dispatch import receiver
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

@receiver(user_logged_in)
def logged_in_message(user, request, **kwargs):
    """Add a welcome message when the user logs in """
    messages.success(request, 'User {user} successfully logged in'.format(user=user.username))

def weight_validator(weight):
    if not (-255 <= weight <= 255):
        raise ValidationError('Weight is -255 to 255')

class SmallIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if 'mysql' in connection.settings_dict['ENGINE']:
            return 'smallint'
        else:
            return super(SmallIntegerField, self).db_type(connection)


class CommonModel(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', editable=False)
    active = models.BooleanField(default=True)
    site = models.ForeignKey(Site, editable=False)


class Rule(CommonModel):

    class Meta:
        ordering = ['id', ]
        # index_together = [ ["start_sort", "end_sort"], ] # doesnt offer a performance advantage

    RULE_CHOICE = (('MOD10', 'MOD10'), ('MOD11', 'MOD11'), ('DBLAL', 'DBLAL'))

    start_sort = models.CharField(max_length=6, db_index=True, help_text=_('from this sort code'))
    end_sort = models.CharField(max_length=6, db_index=True, help_text=_('to this sort code'))
    mod_rule = models.CharField(max_length=255, choices=RULE_CHOICE, help_text=_('determine which algorithm to apply'))
    mod_exception = models.CharField(max_length=2, blank=True, help_text=_('exception rule'))
    weight = ArrayField(models.SmallIntegerField(validators=[weight_validator]), size=14, verbose_name='Weights')

    objects = models.Manager()  # objects manager accesses all, site manager access rows for current site
    current = CurrentSiteManager('site')


    def __str__(self):
        return 'id={0} {1}-{2} {3}'.format(self.id, self.start_sort, self.end_sort, self.mod_rule)

    # def delete(self, using=None, keep_parents=None):  # turn physical delete requests into logical deletes
    #     if self.active:
    #         self.active = False
    #         self.save()
    #     else:
    #         super(Rule, self).delete()

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

@transaction.atomic()
def load_rules(filename: str, sort_codes=None):
    if 'http' in filename:
        response, content = httplib2.Http('.cache').request(filename)
        if response.status not in (200, 301):
            raise RuntimeError('%s %s' % (response.status, response.reason))
        f = content.decode("utf-8").split('\r\n')
    else:
        filename = path.join(settings.MEDIA_ROOT, filename).replace('..', '')
        f = open(filename, "r")
    Rule.objects.all().delete()
    user_model = get_user_model()
    user = user_model.objects.first()
    site = Site.objects.get_current()
    insert_list = []
    for counter, line in enumerate(f):
        if line and (sort_codes is None or any(line[0:6] <= sort_code <= line[7:13] for sort_code in sort_codes)):
            items = [item for item in line.strip().split()]
            try:
                mod_exception = items[17]
            except IndexError:
                mod_exception = ''
            insert_list.append(Rule(start_sort=items[0], end_sort=items[1], mod_rule=items[2],
                                    weight=[items[w] for w in range(3,17)], mod_exception=mod_exception,
                                    created_by=user, updated_by=user, site=site))
    Rule.objects.bulk_create(insert_list)
    return counter
