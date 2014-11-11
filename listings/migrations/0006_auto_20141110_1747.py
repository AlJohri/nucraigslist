# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20141110_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_text',
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='listing',
            name='message',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]