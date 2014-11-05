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

        for obj in get_feed(api, "357858834261047", start=parse("10-1-2014"), end=parse("11-1-2014")):
            print "-----------------------------------------------------"
            print obj['id'], obj['created_time'], obj['updated_time'] #, obj['message']

            if User.objects.filter(uid=obj['from']['id']).count():
                u = User.objects.get(uid=obj['from']['id'])
            else:
                u = User(name = obj['from']['name'], uid=obj['from']['id'])
                u.save()
            l = Listing(listing_text = obj['message'], pub_date = timezone.now(), seller = u)
            Command.filter_listing(l)
            l.save()

            if 'comments' in obj:
                for comment in obj['comments']['data']:
                    if User.objects.filter(uid=comment['from']['id']).count():
                        commenter = User.objects.get(uid=comment['from']['id'])
                        print commenter.uid
                    else:
                        commenter = User(name = comment['from']['name'], uid=comment['from']['id'])
                        commenter.save()
                    comment=Comment(comment_text = comment['message'], pub_date = timezone.now(), user = commenter, listing = l)
                    comment.save()
            else:
                comments = None

            # self.stdout.write('Successfully closed poll "%s"' % poll_id)

    @staticmethod
    def filter_listing(listing):
        count=0
        text = listing.listing_text.lower()
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