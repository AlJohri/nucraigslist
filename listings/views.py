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