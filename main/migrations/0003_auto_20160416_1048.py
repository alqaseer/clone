# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160416_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=b'uploads/'),
        ),
    ]
