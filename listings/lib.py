from listings.models import Listing, User, Comment

from dateutil.parser import parse
from django.utils import timezone

def get_fb_graph_api():
	from facebook import GraphAPI, GraphAPIError
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
	print "-----------------------------------------------------"
	print listing_obj['id'], listing_obj['updated_time'], listing_obj['updated_time'] #, listing_obj['message']

	import pdb; pdb.set_trace()
	
	listing_obj['id'] = listing_obj['id'].split("_")[-1]
	listing_obj['created_time'] = parse(listing_obj['created_time'])
	listing_obj['updated_time'] = parse(listing_obj['updated_time'])

	user = User.objects.filter(id=listing_obj['from']['id']).first() or User.objects.create(id=listing_obj['from']['id'], name = listing_obj['from']['id'])
	listing = Listing.objects.filter(id=listing_obj['id']).first() or Listing.objects.create(id = listing_obj['id'], message = listing_obj.get('message'), created_time = listing_obj['created_time'], updated_time = listing_obj['updated_time'], seller = user)

	for comment_obj in listing_obj.get('comments', {}).get('data', []):
		comment['created_time'] = parse(comment_obj['created_time'])
		commenter = User.objects.filter(id=comment_obj['from']['id']).first() or User.objects.create(id=comment_obj['from']['id'], name = comment_obj['from']['id'])
		comment = Comment.objects.filter(id=comment_obj['id']).first() or Comment.objects.create(id = comment_obj['id'], message = comment_obj.get('message'), created_time = comment_obj['created_time'], user = commenter, listing = listing)