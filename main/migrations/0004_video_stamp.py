# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160416_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='stamp',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
