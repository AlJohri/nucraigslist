from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys, re, csv, requests
from dateutil.parser import parse
from django.utils import timezone
from optparse import make_option

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
    )

    def handle(self, *args, **options):

        print "Downloading word bank.."

        word_bank = {}
        response = requests.get("https://docs.google.com/spreadsheets/d/1vX1U4SjXDf4--P4iUg1e3apDMYhRh74xogAn6bIf5R4/export?format=csv")
        reader = csv.DictReader(response.content.split('\n'), delimiter=',')
        for row in reader:
            for column, value in row.iteritems():
                if value:
                    word_bank.setdefault(column, []).append(value)

        print word_bank

        print "Download complete."

        if options['all']:
            listings = Listing.objects.all()
        else:
            listings = Listing.objects.filter(parsed=False)

        print "Parsing %d Listings.." % listings.count()

        for listing in listings:
            Command.filter_listing(listing, word_bank)
            listing.parsed = True
            listing.save()

        print "Parsing complete."


    @staticmethod
    def filter_listing(listing, word_bank):

        buy_sell_bank = {
            'buying' : 100,
            'looking' : 75,
            '.+\?' : 100,
            'does' : 40,
            'anyone' : 50,
            'anybody' : 50,
            '\$.*' : -100,
            'obo' : -100,
            'selling' : -25,
            'sale' : -50,
            '\d+' : -90, #posts containing number are generally prices
        }

        count = 0

        for word in listing.message.lower().split():
            for category, regexes in word_bank.items():
                for reg in regexes:
                    if re.match(reg, word):
                        listing.category = category
                        print "[" + listing.category + "]", listing.message.replace("\n", "")[:150]
                        break

            for reg, value in buy_sell_bank.items():
                if re.match(reg, word):
                    count += value

        if not listing.category:
            print "[None]", listing.message.replace("\n", "")[:150]


        if count > 0: listing.buy_or_sell = 'buy'
        elif count < 0: listing.buy_or_sell = 'sell'
