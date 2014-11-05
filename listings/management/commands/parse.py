from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys, re
from dateutil.parser import parse
from django.utils import timezone

class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
    	Command.filter_listing(l)

    @clasmethod
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
            '\d+' : -90, #posts containing number are generally prices
        }

        item_bank = {
            'tickets?' : 'tickets',
            'tix' : 'tickets',
            'mattress(es)?' : 'bedding',
            'twin' : 'bedding',
            'queen' : 'bedding',
            'king' : 'bedding',
            'bikes?' : 'bicycles',
            'bicycles?' : 'bicycles',
            '.*phone' : 'phones',
            'keys?' : 'trash',
        }
        #noise_list = ['to','a','an','and','for','please','thanks','thank','you','some','on','if','me','or','that','that\'s','out','of','so','i','ill','i\'ll','be','my','into','the']
        text_list = text.split()
        ##text_list=' '.join([i for i in text_list if i not in noise_list])
        for word in text_list:
            for k, v in item_bank.items():
                if re.match(k, word):
                    listing.category=v
            for k, v in buy_sell_bank.items():
                if re.match(k, word):
                    count+=v
                    print(text_list)
                    print("k is: " + k)
                    print (count)
        if count>0: listing.buy_or_sell='buy'
        elif count <0: listing.buy_or_sell='sell'