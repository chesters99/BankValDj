# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 14:00
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import rules.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('start_sort', models.CharField(db_index=True, help_text='from this sort code', max_length=6)),
                ('end_sort', models.CharField(db_index=True, help_text='to this sort code', max_length=6)),
                ('mod_rule', models.CharField(choices=[('MOD10', 'MOD10'), ('MOD11', 'MOD11'), ('DBLAL', 'DBLAL')], help_text='determine which algorithm to apply', max_length=255)),
                ('mod_exception', models.CharField(blank=True, help_text='exception rule', max_length=2)),
                ('weight', django.contrib.postgres.fields.ArrayField(base_field=models.SmallIntegerField(validators=[rules.models.weight_validator]), size=14, verbose_name='Weights')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current', django.contrib.sites.managers.CurrentSiteManager('site')),
            ],
        ),
    ]