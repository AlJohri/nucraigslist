import os, re, sys, json, pprint
import environment

pp = pprint.PrettyPrinter(indent=4)

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.graphapi import get_feed

from dateutil.parser import parse

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

api = GraphAPI(FACEBOOK_USER_TOKEN)

try:
	api.get_object('me')
except GraphAPIError as e:
	print e
	print "Update and source your .secret file"
	sys.exit()

for item in get_feed(api, "357858834261047", start=parse("4-1-2014"), end=parse("4-2-2014")):
	print "-----------------------------------------------------"
	print item['id'], item['created_time'], item['updated_time']
	print item['message']