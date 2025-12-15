# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nodewatcher.core.registry.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cgm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='throughputinterfacelimitconfig',
            name='limit_in',
            field=nodewatcher.core.registry.fields.RegistryChoiceField('node.config', 'core.interfaces.limits#speeds', default='', max_length=50, verbose_name='Download limit', blank=True, choices=[('128', '128 Kbit/s'), ('256', '256 Kbit/s'), ('512', '512 Kbit/s'), ('1024', '1 Mbit/s'), ('2048', '2 Mbit/s'), ('4096', '4 Mbit/s'), ('6144', '6 Mbit/s'), ('8192', '8 Mbit/s'), ('10240', '10 Mbit/s'), ('15360', '15 Mbit/s'), ('20480', '20 Mbit/s'), ('25600', '25 Mbit/s'), ('30720', '30 Mbit/s'), ('40960', '40 Mbit/s'), ('51200', '50 Mbit/s'), ('61440', '60 Mbit/s'), ('71680', '70 Mbit/s'), ('81920', '80 Mbit/s'), ('92160', '90 Mbit/s'), ('102400', '100 Mbit/s')]),
        ),
        migrations.AlterField(
            model_name='throughputinterfacelimitconfig',
            name='limit_out',
            field=nodewatcher.core.registry.fields.RegistryChoiceField('node.config', 'core.interfaces.limits#speeds', default='', max_length=50, verbose_name='Upload limit', blank=True, choices=[('128', '128 Kbit/s'), ('256', '256 Kbit/s'), ('512', '512 Kbit/s'), ('1024', '1 Mbit/s'), ('2048', '2 Mbit/s'), ('4096', '4 Mbit/s'), ('6144', '6 Mbit/s'), ('8192', '8 Mbit/s'), ('10240', '10 Mbit/s'), ('15360', '15 Mbit/s'), ('20480', '20 Mbit/s'), ('25600', '25 Mbit/s'), ('30720', '30 Mbit/s'), ('40960', '40 Mbit/s'), ('51200', '50 Mbit/s'), ('61440', '60 Mbit/s'), ('71680', '70 Mbit/s'), ('81920', '80 Mbit/s'), ('92160', '90 Mbit/s'), ('102400', '100 Mbit/s')]),
        ),
    ]
