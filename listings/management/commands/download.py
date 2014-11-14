from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys
from django.utils import timezone
from optparse import make_option
from listings.lib import save_obj, get_fb_graph_api
from dateutil.parser import parse

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    option_list = BaseCommand.option_list + (
        make_option('--recent',
            action='store_true',
            dest='recent',
            default=True,
            help='TODO add more helpful text'
        ),
    )

    def handle(self, *args, **options):

        api = get_fb_graph_api()

        # if not options['reverse']:
        #     try:
        #         latest_listing_time = Listing.objects.order_by('-updated_time')[:1][0].updated_time.replace(tzinfo=None)
        #     except Exception as e:
        #         latest_listing_time = parse("01-1-2012")
        #     current_time = timezone.now().replace(tzinfo=None)
        # else:
        latest_listing_time = parse("01-1-2012")
        current_time = Listing.objects.order_by('updated_time')[:1][0].updated_time.replace(tzinfo=None)

        print "Downloading from ", latest_listing_time, "to", current_time, "in reverse chronological order (latest first)."
        for obj in get_feed(api, "357858834261047", start=latest_listing_time, end=current_time):
            save_obj(obj)
