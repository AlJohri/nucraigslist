from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment
from optparse import make_option

from listings.lib import get_word_bank, filter_listing

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Parse all listings instead of just unparsed'
        ),
        make_option('--blank',
            action='store_true',
            dest='blank',
            default=False,
            help='Parse listings with category=None'
        ),
        make_option('--dl',
            action='store_true',
            dest='dl',
            default=False,
            help='Redownload word bank'
        ),
    )

    def handle(self, *args, **options):

        word_bank = get_word_bank(dl=True)

        if options['all']: listings = Listing.objects.all()
        elif options['blank']: listings = Listing.objects.filter(category=None)
        else: listings = Listing.objects.filter(parsed=False)

        print "Parsing %d Listings.." % listings.count()
        for i, listing in enumerate(listings): filter_listing(listing, word_bank, i)
        print "Parsing complete."
