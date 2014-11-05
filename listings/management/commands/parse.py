from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys, re
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

        if options['all']:
            listings = Listing.objects.all()
        else:
            listings = Listing.objects.filter(parsed=False)

        for listing in listings:
    	   Command.filter_listing(listing)
           listing.parsed = True
           listing.save()

    @staticmethod
    def filter_listing(listing):
        count=0
        text = listing.message.lower()
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
            '\d+' : -90, #posts containing numbers are generally prices
        }

        item_bank = {
            'tickets': ['tickets?', 'tix'],
            'bedding': ['mattress(es)?', 'twin', 'queen', 'king'],
            'bicycles': ['bikes?', 'bicycles?'],
            'phones': ['.*phone'],
            'trash': ['keys?']
        }

        #noise_list = ['to','a','an','and','for','please','thanks','thank','you','some','on','if','me','or','that','that\'s','out','of','so','i','ill','i\'ll','be','my','into','the']
        text_list = text.split()
        ##text_list=' '.join([i for i in text_list if i not in noise_list])
        for word in text_list:
            for category, regexes in item_bank.items():
                for reg in regexes:
                    if re.match(reg, word):
                        listing.category=v
                        break

            for reg, value in buy_sell_bank.items():
                if re.match(reg, word):
                    count += value
                    print text_list
                    print "k is: " + k
                    print count

        if count > 0: listing.buy_or_sell = 'buy'
        elif count < 0: listing.buy_or_sell = 'sell'
