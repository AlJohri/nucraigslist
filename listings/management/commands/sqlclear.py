from django.db import connection

from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import unicodecsv as csv

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        """
        this command is a work in progress, please use carefully
        """

        cursor = connection.cursor()
        cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
        parts = ('DROP TABLE IF EXISTS %s CASCADE;' % table for (table,) in cursor.fetchall())
        # sql = 'SET FOREIGN_KEY_CHECKS = 0;\n' + '\n'.join(parts) + '\n' + 'SET FOREIGN_KEY_CHECKS = 1;\n'

        print '\n'.join(parts)
