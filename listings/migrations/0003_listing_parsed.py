# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20141104_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='parsed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
