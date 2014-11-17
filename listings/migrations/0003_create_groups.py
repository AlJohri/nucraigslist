# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_groups(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Group = apps.get_model("listings", "Group")
    Group.objects.create(id=357858834261047, school="Northwestern University", name="Free & For Sale")
    Group.objects.create(id=633074646739463, school="Northwestern University", name="NU Closet Recycle")
    Group.objects.create(id=357858800927717, school="Northwestern University", name="Textbook Exchange")
    Group.objects.create(id=357858827594381, school="Northwestern University", name="Housing")

class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_make_relations'),
    ]

    operations = [
    	migrations.RunPython(create_groups),
    ]
