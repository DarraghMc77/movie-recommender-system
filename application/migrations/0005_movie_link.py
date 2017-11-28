# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='link',
            field=models.CharField(max_length=256, default=''),
            preserve_default=False,
        ),
    ]
