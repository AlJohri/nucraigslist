from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, sys, re, csv, requests, nltk
from dateutil.parser import parse
from django.utils import timezone
from optparse import make_option

from nltk.tokenize import RegexpTokenizer

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

        if not os.path.isfile("word_bank.csv") or os.path.getsize("word_bank.csv") == 0 or options['dl']:
            print "Downloading word bank.."
            response = requests.get("https://docs.google.com/spreadsheets/d/1vX1U4SjXDf4--P4iUg1e3apDMYhRh74xogAn6bIf5R4/export?format=csv")
            with open("word_bank.csv", "w") as f: f.write(response.content)
            print "Download complete."

        word_bank_csv =  open("word_bank.csv", "r")
        word_bank = {}

        reader = csv.DictReader(word_bank_csv)
        for row in reader:
            for column, value in row.iteritems():
                if value:
                    word_bank.setdefault(column, []).append(value)

        print word_bank

        if options['all']: listings = Listing.objects.all()
        elif options['blank']: listings = Listing.objects.filter(category=None)
        else: listings = Listing.objects.filter(parsed=False)

        print "Parsing %d Listings.." % listings.count()

        for listing in listings:
            Command.filter_listing(listing, word_bank)
            listing.parsed = True
            listing.save()

        print "Parsing complete."


    @staticmethod
    def filter_listing(listing, word_bank):

        def find_category(ngrams):
            for ngram in ngrams:
                for category, regexes in word_bank.items():
                    for reg in regexes:
                        if re.match(r"\b" + reg + r"\b", ngram):
                            return category

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

        tokenizer = RegexpTokenizer(r'\w+')
        unigrams = [x.lower() for x in tokenizer.tokenize(listing.message)]
        bigrams = [" ".join(x) for x in nltk.bigrams(unigrams)]
        ngrams = unigrams + bigrams

        category = find_category(ngrams)
        listing.category = category

        for ngram in unigrams:
            for reg, value in buy_sell_bank.items():
                if re.match(reg, ngram):
                    count += value

        if count > 0: listing.buy_or_sell = 'buy'
        elif count < 0: listing.buy_or_sell = 'sell'

        print "[" + str(listing.category) + "," + str(listing.buy_or_sell) + "]", listing.id, listing.message.replace("\n", "")[:150]
