from django.contrib import admin
from listings.models import User, Listing, Comment

class CommentsInline(admin.TabularInline):
	model = Comment

class ListingAdmin(admin.ModelAdmin):
	fields = ['listing_text', 'pub_date', 'approved', 'seller', 'buy_or_sell', 'category']
	list_filter = ['buy_or_sell']
	inlines = [CommentsInline]

admin.site.register(Listing, ListingAdmin)

class UserAdmin(admin.ModelAdmin):
	fields = ['name', 'uid']

admin.site.register(User, UserAdmin)