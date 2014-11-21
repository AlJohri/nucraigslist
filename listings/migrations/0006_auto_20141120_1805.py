# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_listing_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='seller',
            new_name='user',
        ),
    ]
