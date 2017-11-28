# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20150315_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
