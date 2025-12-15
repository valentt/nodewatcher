# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nodewatcher.core.registry.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cgm', '0004_auto_20150919_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileinterfaceconfig',
            name='device',
            field=nodewatcher.core.registry.fields.RegistryChoiceField('node.config', 'core.interfaces#mobile_device', default='ppp0', max_length=50, choices=[('ppp0', 'PPP over USB0'), ('qmi0', 'QMI over USB0')]),
        ),
    ]
