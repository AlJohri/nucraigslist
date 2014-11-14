from __future__ import absolute_import
from celery import shared_task
from listings.models import Listing, User, Comment
import os

from listings.lib import save_obj, get_fb_graph_api, get_word_bank, filter_listing

api = get_fb_graph_api()
word_bank = get_word_bank(dl=True)

@shared_task
def download():
	feed = api.get_object("357858834261047/feed")
	for i,obj in enumerate(feed['data']):
		listing = save_obj(obj)
		filter_listing(listing, word_bank, i)
