# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('type', models.CharField(max_length=6)),
                ('message', models.CharField(default=b'', max_length=400)),
                ('approved', models.BooleanField(default=False)),
                ('buy_or_sell', models.CharField(max_length=4, null=True)),
                ('category', models.CharField(max_length=15, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(to='listings.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(to='listings.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='listings.User'),
            preserve_default=True,
        ),
    ]
