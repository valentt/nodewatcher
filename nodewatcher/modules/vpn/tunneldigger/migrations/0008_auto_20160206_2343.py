# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-06 22:43
from __future__ import unicode_literals

import datetime
from django.db import migrations
import timedelta.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_tunneldigger', '0007_auto_20151018_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tunneldiggerbrokerconfig',
            name='tunnel_timeout',
            field=timedelta.fields.TimedeltaField(choices=[(datetime.timedelta(0, 60), '1 minute'), (datetime.timedelta(0, 120), '2 minutes'), (datetime.timedelta(0, 300), '5 minutes')], default=b'1min', verbose_name='Tunnel Timeout'),
        ),
    ]
