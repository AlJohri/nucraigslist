from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import unicodecsv as csv

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        with open("export.csv", 'w') as f:
            writer = csv.writer(f)
            header = ['id', 'created_time', 'updated_time', 'text']
            writer.writerow(header)
            for listing in Listing.objects.all():
                writer.writerow([listing.id, listing.created_time, listing.updated_time, listing.message])
