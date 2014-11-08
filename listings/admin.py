from django.contrib import admin
from listings.models import User, Listing, Comment

with open("word_bank.csv") as f:
	categories = f.readline().rstrip("\n").split(",")

def make_action(field, value):
    name = 'mark_%s' % value
    action = lambda modeladmin, request, queryset: queryset.update(field=value)
    action.short_description = "Mark selections as %s %s" % (field, value)
    return (name, (action, name, action.short_description))

def make_category_actions():
	return [make_action("category", category) for category in categories]

def make_approved_action():
	return [make_action("approved", True)]

class CommentsInline(admin.TabularInline):
	model = Comment

class ListingsInline(admin.TabularInline):
	model = Listing

class ListingAdmin(admin.ModelAdmin):
	fields = ['id', 'created_time', 'updated_time', 'type', 'message', 'seller', 'approved', 'buy_or_sell', 'category', 'sold']
	list_filter = ['buy_or_sell', 'created_time', 'updated_time', 'category', 'approved']
	list_display = ['id', 'message', 'category', 'created_time']
	search_fields = ['message']
	inlines = [CommentsInline]

	def get_actions(self, request):
		return dict(make_category_actions() + make_approved_action())

admin.site.register(Listing, ListingAdmin)

class UserAdmin(admin.ModelAdmin):
	fields = ['name', 'id']
	search_fields = ['name']
	inlines = [ListingsInline]

admin.site.register(User, UserAdmin)