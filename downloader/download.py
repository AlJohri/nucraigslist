import os, re, sys, json, pprint
from dateutil.parser import parse
import environment

from blessings import Terminal
t = Terminal()

from pymongo import MongoClient
from pymongo import errors
client = MongoClient()
db = client.nucraigslist
posts = db.posts

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

for item in get_feed(api, "357858834261047", start=parse("10-1-2014"), end=parse("11-1-2014")):
    print "-----------------------------------------------------"
    print item['id'], item['created_time'], item['updated_time']
    item['_id'] = item['id']
    del item['id']

    try:
        posts.insert(item)
    except errors.DuplicateKeyError:
        print t.red("%s already exists in the database" % item['_id'])
        continue