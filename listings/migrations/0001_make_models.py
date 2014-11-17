# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # replaces = [(b'listings', '0001_initial'), (b'listings', '0002_auto_20141104_2359'), (b'listings', '0003_listing_parsed'), (b'listings', '0004_listing_sold'), (b'listings', '0005_auto_20141110_1722'), (b'listings', '0006_auto_20141110_1747'), (b'listings', '0007_auto_20141110_1759'), (b'listings', '0008_auto_20141113_1522'), (b'listings', '0009_auto_20141113_1819'), (b'listings', '0010_auto_20141113_1936')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('type', models.CharField(max_length=6)),
                ('message', models.TextField(default=b'', blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('buy_or_sell', models.CharField(max_length=4, null=True)),
                ('category', models.CharField(max_length=15, null=True)),
                ('parsed', models.BooleanField(default=False)),
                ('sold', models.BooleanField(default=False)),
                ('picture', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('message', models.TextField(default=b'', blank=True)),
                ('created_time', models.DateTimeField(verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
