from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys, re
from dateutil.parser import parse
from django.utils import timezone

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        from facebook import GraphAPI, GraphAPIError
        from socialscraper.facebook.graphapi import get_feed
        FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
        api = GraphAPI(FACEBOOK_USER_TOKEN)

        try:
            api.get_object('me')
        except GraphAPIError as e:
            print e
            print "Update and source your .secret file"
            sys.exit()

        try:
            latest_listing_time = Listing.objects.order_by('-created_time')[:1][0].updated_time.replace(tzinfo=None)
        except Exception as e:
            print e
            latest_listing_time = parse("01-1-2012")

        current_time = timezone.now().replace(tzinfo=None)

        print "Downloading from ", latest_listing_time, "to", current_time, "in reverse chronological order (latest first)."

        for obj in get_feed(api, "357858834261047", start=latest_listing_time, end=current_time):
            print "-----------------------------------------------------"
            print obj['id'], obj['created_time'], obj['updated_time'] #, obj['message']

            print obj

            if User.objects.filter(id=obj['from']['id']).count():
                user = User.objects.get(id=obj['from']['id'])
            else:
                user = User(
                    id=obj['from']['id'],
                    name = obj['from']['name']
                )
                user.save()
            
            listing = Listing(
                id = obj['id'].split("_")[-1],
                message = obj.get('message') or '',
                created_time = parse(obj['created_time']),
                updated_time = parse(obj['updated_time']),
                seller = user
            )
            listing.save()

            if 'comments' in obj:
                for comment in obj['comments']['data']:
                    if User.objects.filter(id=comment['from']['id']).count():
                        commenter = User.objects.get(id=comment['from']['id'])
                        print commenter.id
                    else:
                        commenter = User(name = comment['from']['name'], id=comment['from']['id'])
                        commenter.save()
                    comment=Comment(
                        comment_text = comment.get('message') or '',
                        pub_date = timezone.now(), 
                        user = commenter, 
                        listing = listing
                    )
                    comment.save()
            else:
                comments = None

            # self.stdout.write('Successfully closed poll "%s"' % poll_id)