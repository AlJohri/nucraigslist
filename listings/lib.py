from listings.models import Listing, User, Comment

from dateutil.parser import parse
from django.utils import timezone
from facebook import GraphAPI, GraphAPIError
import os, sys, requests, csv, re, nltk

from nltk.tokenize import RegexpTokenizer

def get_word_bank(dl=False):
    if not os.path.isfile("word_bank.csv") or os.path.getsize("word_bank.csv") == 0 or dl:
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

    word_bank_csv.close()

    return word_bank

def get_fb_graph_api():
    FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
    api = GraphAPI(FACEBOOK_USER_TOKEN)

    try:
        api.get_object('me')
    except GraphAPIError as e:
        print e
        print "Update and source your .secret file"
        sys.exit()

    return api

def save_obj(listing_obj):
    # print "-----------------------------------------------------"
    # print listing_obj['id'], listing_obj['updated_time'], listing_obj['updated_time'] #, listing_obj['message']
    
    listing_obj['id'] = listing_obj['id'].split("_")[-1]
    listing_obj['created_time'] = parse(listing_obj['created_time'])
    listing_obj['updated_time'] = parse(listing_obj['updated_time'])

    user = User.objects.filter(id=listing_obj['from']['id']).first() or User.objects.create(id=listing_obj['from']['id'], name = listing_obj['from']['id'])
    listing = Listing.objects.filter(id=listing_obj['id']).first() or Listing.objects.create(id = listing_obj['id'], message = listing_obj.get('message'), created_time = listing_obj['created_time'], updated_time = listing_obj['updated_time'], seller = user)

    print "[listing] %s - %s" % (user, listing)

    for comment_obj in listing_obj.get('comments', {}).get('data', []):
        comment_obj['created_time'] = parse(comment_obj['created_time'])
        commenter = User.objects.filter(id=comment_obj['from']['id']).first() or User.objects.create(id=comment_obj['from']['id'], name = comment_obj['from']['id'])
        comment = Comment.objects.filter(id=comment_obj['id']).first() or Comment.objects.create(id = comment_obj['id'], message = comment_obj.get('message'), created_time = comment_obj['created_time'], user = commenter, listing = listing)

        print "[comment] %s - %s" % (commenter, comment)

    return listing

def filter_listing(listing, word_bank, index):

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

    listing.parsed = True
    listing.save()

    print str(index) + ": [" + str(listing.category) + "," + str(listing.buy_or_sell) + "]", listing.id, listing.message.replace("\n", "")[:150]
