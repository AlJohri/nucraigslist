# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_listing_parsed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
