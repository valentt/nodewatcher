# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nodewatcher.core.registry.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', nodewatcher.core.registry.fields.RegistryChoiceField('node.config', 'core.type#type', max_length=50, null=True, choices=[('server', 'Server'), ('backbone', 'Backbone'), ('wireless', 'Wireless'), ('test', 'Test'), ('mobile', 'Mobile'), ('dead', 'Dead'), (None, 'Unknown')])),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_types.typeconfig_set+', editable=False, to='contenttypes.ContentType', null=True)),
                ('root', models.ForeignKey(related_name='config_types_typeconfig', editable=False, to='core.Node')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
    ]
