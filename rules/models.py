import httplib2
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


def logged_in_message(user, request, **kwargs):
    """Add a welcome message when the user logs in """
    messages.success(request, "User '%s' successfully logged in" % user.username)

user_logged_in.connect(logged_in_message)


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
    def weight_validator(weight):
        if not (-255 <= weight <= 255):
            raise ValidationError("Weight is -255 to 255")

    MODULUS_10 = 'MOD10'
    MODULUS_11 = 'MOD11'
    DOUBLE_ALT = 'DBLAL'
    RULE_CHOICE = ((MODULUS_10, MODULUS_10), (MODULUS_11, MODULUS_11), (DOUBLE_ALT, DOUBLE_ALT))

    start_sort = models.CharField(max_length=6, db_index=True, help_text=_('from this sort code'))
    end_sort = models.CharField(max_length=6, db_index=True, help_text=_('to this sort code'))
    mod_rule = models.CharField(max_length=255, choices=RULE_CHOICE, help_text=_('determine which algorithm to apply'))
    mod_exception = models.CharField(max_length=2, blank=True, help_text=_('exception rule'))
    weight = ArrayField(models.SmallIntegerField(validators=[weight_validator]), blank=True, size=14)
    # objects manager accesses all records, site manager access only records for the current site
    objects = models.Manager()
    current = CurrentSiteManager('site')

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return '%s %s-%s' % (self.id, self.start_sort, self.end_sort)

    def delete(self, using=None, keep_parents=None):  # turn physical delete requests into logical deletes
        if self.active:
            self.active = False
            self.save()

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


def get_rules(filename: str, sort_code=None):
    try:
        if 'http:' in filename:
            response, content = httplib2.Http('.cache').request(filename)
            if response.status not in (200, 301):
                raise RuntimeError('%s %s' % (response.status, response.reason))
            rows = [line.strip() for line in content.decode("utf-8").split('\r\n')
                    if line.strip() and line[0:5] <= (sort_code or line[0:5]) <= line[7:12]]
        else:
            with open(filename, "r") as f:
                rows = [line.strip() for line in f
                        if line.strip() and line[0:5] <= (sort_code or line[0:5]) <= line[7:12]]
    except (IOError, RuntimeError):
        return None
    return rows


def load_rules(rows: dict):
    """ load all templates (if sort code is None) or load templates applicable to a specific sort code
    :param rows: dict
    """
    Rule.objects.all().delete()
    rule = {}
    for row in rows:
        line_list = [item for item in row.split()]
        rule["start_sort"] = line_list[0]
        rule["end_sort"] = line_list[1]
        rule["mod_rule"] = line_list[2]
        rule["weight"] = [line_list[w] for w in range(3,17)]
        try:
            rule["mod_exception"] = line_list[17]
        except IndexError:
            rule["mod_exception"] = ''
        Rule.objects.create(**rule)
    return len(rows)
