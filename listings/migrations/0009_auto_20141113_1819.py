# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_auto_20141113_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
