from __future__ import absolute_import
from celery import shared_task
from listings.models import Listing, User, Comment, Group
import os

from listings.lib import save_obj, get_fb_graph_api, get_word_bank, filter_listing

api = get_fb_graph_api()
word_bank = get_word_bank(dl=False)

@shared_task
def download():
	for group in Group.objects.all():
		feed = api.get_object("%s/feed" % group.id)
		for i,obj in enumerate(feed['data']):
			listing, listing_created = save_obj(obj)
			if listing_created: filter_listing(listing, word_bank, i)
