from __future__ import absolute_import
from celery import shared_task
from listings.models import Listing, User, Comment
import os

from listings.lib import save_obj, get_fb_graph_api

api = get_fb_graph_api()

@shared_task
def download():
	feed = api.get_object("357858834261047/feed")
	for obj in feed['data']:
		save_obj(obj)