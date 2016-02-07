# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='generalmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='generalresourcesmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='interfacemonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='networkaddressmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='networkresourcesmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='routingannouncemonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='routingtopologymonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='rttmeasurementmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
        migrations.AddField(
            model_name='systemstatusmonitor',
            name='annotations',
            field=jsonfield.JSONField(default={}, help_text='Enter a valid JSON object', editable=False),
        ),
    ]
