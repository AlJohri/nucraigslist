from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing, User, Comment

import os, time
import unicodecsv as csv
from dateutil.parser import parse
from django.utils import timezone

class Command(BaseCommand):
	# args = '<poll_id poll_id ...>'
	# help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):

		from facebook import GraphAPI, GraphAPIError
		FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
		api = GraphAPI(FACEBOOK_USER_TOKEN)

		try:
			api.get_object('me')
		except GraphAPIError as e:
			print e
			print "Update and source your .secret file"
			sys.exit()

		while True:
			feed = api.get_object("357858834261047/feed")
			for obj in feed['data']:
				print "-----------------------------------------------------"
				print obj['id'], obj['updated_time'], obj['updated_time'] #, obj['message']

				if User.objects.filter(id=obj['from']['id']).count():
					user = User.objects.get(id=obj['from']['id'])
				else:
					user = User(
						id=obj['from']['id'],
						name = obj['from']['name']
					)
					user.save()
					print "new user", user.name
				
				if Listing.objects.filter(id=obj['id'].split("_")[-1]).count():
					print "listing exists", obj['id'].split("_")[-1]
				else:
					listing = Listing(
						id = obj['id'].split("_")[-1],
						message = obj.get('message') or '',
						created_time = parse(obj['created_time']),
						updated_time = parse(obj['updated_time']),
						seller = user
					)
					listing.save()
					print "new listing", listing.id

					# currently only creates comments for new listings
					# need to store comment ids.....!!!

					if 'comments' in obj:
						for comment in obj['comments']['data']:
							if User.objects.filter(id=comment['from']['id']).count():
								commenter = User.objects.get(id=comment['from']['id'])
								print commenter.id
							else:
								commenter = User(name = comment['from']['name'], id=comment['from']['id'])
								commenter.save()
							comment=Comment(
								message = comment.get('message') or '',
								pub_date = timezone.now(), 
								user = commenter, 
								listing = listing
							)
							comment.save()
					else:
						comments = None
			time.sleep(5)