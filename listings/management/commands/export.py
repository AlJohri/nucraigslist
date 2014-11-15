from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import unicodecsv as csv

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        with open("listings.csv", 'w') as f:
            writer = csv.writer(f)
            header = ['id', 'created_time', 'updated_time', 'category', '# comments', 'text', 'picture_link']
            writer.writerow(header)
            for listing in Listing.objects.all():
            	row = [listing.id, listing.created_time, listing.updated_time, listing.category, listing.comments.count(), listing.message]
                writer.writerow(row)
                print row

        with open("comments.csv", 'w') as f:
            writer = csv.writer(f)
            header = ['id', 'listing_id', 'created_time', 'text']
            writer.writerow(header)
            for comment in Comment.objects.all():
            	row = [comment.id, comment.listing.id, comment.created_time, comment.message]
                writer.writerow(row)
                print row
