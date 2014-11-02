from django.shortcuts import render, get_object_or_404
import json
import os
import re
from django.utils import timezone

from listings.models import Listing, User, Comment

def index(request):
	#get_listings()
	latest_listings_list = Listing.objects.order_by('-pub_date')
	bedding_sell_list = Listing.objects.filter(category='bedding', buy_or_sell='sell')
	bedding_buy_list = Listing.objects.filter(category='bedding', buy_or_sell='buy')
	phone_sell_list = Listing.objects.filter(category='phones', buy_or_sell='sell')
	phone_buy_list = Listing.objects.filter(category='phones', buy_or_sell='buy')
	bike_buy_list = Listing.objects.filter(category='bicycles', buy_or_sell='buy')
	bike_sell_list = Listing.objects.filter(category='bicycles', buy_or_sell='sell')
	ticket_sell_list = Listing.objects.filter(category='tickets', buy_or_sell='sell')
	context = {'latest_listings_list' : latest_listings_list, 'bedding_sell_list' : bedding_sell_list, 
				'bedding_buy_list' : bedding_buy_list, 'phone_buy_list' : phone_buy_list, 
				'phone_sell_list' : phone_sell_list, 'bike_buy_list' : bike_buy_list,
				'bike_sell_list' : bike_sell_list, 'ticket_sell_list' : ticket_sell_list}
	return render(request, 'listings/index.html', context)

def detail(request, listing_id):
	listing = get_object_or_404(Listing, pk=listing_id)
	return render(request, 'listings/detail.html', {'listing' : listing})

def get_listings():
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'posts.json')
	json_data = open(file_path)
	data = json.load(json_data)
	json_data.close()
	for obj in data:
		if User.objects.filter(uid=obj['from']['id']).count():
			u = User.objects.get(uid=obj['from']['id'])
		else:
			u = User(name = obj['from']['name'], uid=obj['from']['id'])
			u.save()
		l = Listing(listing_text = obj['message'], pub_date = timezone.now(), seller = u)
		filter_listing(l)
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









