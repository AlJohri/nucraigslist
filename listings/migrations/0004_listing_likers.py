# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_create_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='likers',
            field=models.ManyToManyField(related_name='listings', to='listings.User'),
            preserve_default=True,
        ),
    ]
