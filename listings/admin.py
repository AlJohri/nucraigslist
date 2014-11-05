from django.contrib import admin
from listings.models import User, Listing, Comment

class CommentsInline(admin.TabularInline):
	model = Comment

class ListingAdmin(admin.ModelAdmin):
	fields = ['id', 'created_time', 'updated_time', 'type', 'message', 'seller', 'approved', 'buy_or_sell', 'category']
	list_filter = ['buy_or_sell', 'created_time', 'updated_time']
	list_display = ['id', 'message', 'created_time']
	inlines = [CommentsInline]

admin.site.register(Listing, ListingAdmin)

class UserAdmin(admin.ModelAdmin):
	fields = ['name', 'id']

admin.site.register(User, UserAdmin)