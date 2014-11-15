# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_listing_picture_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture_link',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
