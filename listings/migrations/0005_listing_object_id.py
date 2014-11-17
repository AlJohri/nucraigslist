# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_listing_likers'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='object_id',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
    ]
