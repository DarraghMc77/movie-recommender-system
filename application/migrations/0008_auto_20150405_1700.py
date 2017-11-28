# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20150404_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='actor',
            field=models.CharField(max_length=256, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.CharField(max_length=1024, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=256, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.CharField(max_length=256, default=''),
            preserve_default=False,
        ),
    ]
