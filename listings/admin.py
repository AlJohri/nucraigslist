from django.contrib import admin
from listings.models import User, Listing, Comment

def make_approved(modeladmin, request, queryset):
	queryset.update(approved=True)
make_approved.short_description = "Mark selections as approved"

class CommentsInline(admin.TabularInline):
	model = Comment

class ListingsInline(admin.TabularInline):
	model = Listing

class ListingAdmin(admin.ModelAdmin):
	fields = ['id', 'created_time', 'updated_time', 'type', 'message', 'seller', 'approved', 'buy_or_sell', 'category', 'sold']
	list_filter = ['buy_or_sell', 'created_time', 'updated_time']
	list_display = ['id', 'message', 'created_time']
	actions = [make_approved]
	inlines = [CommentsInline]

admin.site.register(Listing, ListingAdmin)

class UserAdmin(admin.ModelAdmin):
	fields = ['name', 'id']
	inlines = [ListingsInline]

admin.site.register(User, UserAdmin)