from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment, Group

import os, sys
from django.utils import timezone
from optparse import make_option
from listings.lib import save_obj, get_fb_graph_api, get_word_bank, filter_listing
from dateutil.parser import parse

from socialscraper.facebook.graphapi import get_feed

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    option_list = BaseCommand.option_list + (
        make_option('--recent',
            action='store_true',
            dest='recent',
            default=True,
            help='Download most recent posts'
        ),
        make_option('--backfill',
            action='store_true',
            dest='backfill',
            default=False,
            help='Backfill database'
        ),
        make_option('--incomplete',
            action='store_true',
            dest='incomplete',
            default=False,
            help='If incomplete, download from 01-1-2012 to earliest post in database.'
        ),
    )

    def handle(self, *args, **options):

        # hack to make "backfill" and "recent" mutually exclusive
        if options['backfill']: options['recent'] = False

        api = get_fb_graph_api()
        word_bank = get_word_bank(dl=False)

        for group in Group.objects.all():

            print "Downloading posts from %s" % group

            if options['recent']:

                print "Downloading most recent posts (no pagination)"
                feed = api.get_object("%s/feed" % group.id)
                for i,obj in enumerate(feed['data']):
                    listing, listing_created = save_obj(obj)
                    if listing_created: filter_listing(listing, word_bank, i)
                    print ""

            elif options['backfill']:

                start = parse("01-1-2012")

                if Listing.objects.filter(group_id=group.id).count() >= 1:
                    end = Listing.objects.filter(group_id=group.id).earliest('updated_time').updated_time.replace(tzinfo=None)
                else:
                    end = timezone.now().replace(tzinfo=None)

                print "Downloading from ", start, "to", end, "in reverse chronological order (latest first)."
                for i,obj in enumerate(get_feed(api, str(group.id), start=start, end=end)):
                    listing, listing_created = save_obj(obj)
                    if listing_created: filter_listing(listing, word_bank, i)
                    print ""
