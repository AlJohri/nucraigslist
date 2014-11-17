# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_make_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(to='listings.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(related_name='comments', to='listings.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='listings.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listing',
            name='group',
            field=models.ForeignKey(to='listings.Group'),
            preserve_default=False,
        ),
    ]
