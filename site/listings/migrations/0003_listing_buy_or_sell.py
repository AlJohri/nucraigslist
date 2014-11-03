# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20141031_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='buy_or_sell',
            field=models.CharField(max_length=4, null=True),
            preserve_default=True,
        ),
    ]
