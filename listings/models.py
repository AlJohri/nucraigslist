from django.db import models

class Group(models.Model):

	BASE_URL = "https://www.facebook.com/groups/%s"

	def __unicode__(self):
		return self.name

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length = 100)
	school = models.CharField(max_length = 100)

class User(models.Model):

	def __unicode__(self):
		return self.name

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length = 100)

class Listing(models.Model):

	BASE_URL = "https://www.facebook.com/%s/posts/%s"

	def __unicode__(self):
		return self.message or u'No Text'

	id = models.BigIntegerField(primary_key=True)
	created_time = models.DateTimeField(null=False)
	updated_time = models.DateTimeField(null=False)
	type = models.CharField(max_length = 6)
	message = models.TextField(null=False, blank=True, default="")
	picture = models.TextField(null=False, blank=True, default="")

	parsed = models.BooleanField(default=False)
	seller = models.ForeignKey(User)
	approved = models.BooleanField(default=False)
	buy_or_sell = models.CharField(max_length = 4, null=True)
	category = models.CharField(max_length = 15, null=True)
	object_id = models.BigIntegerField(null=True)

	group = models.ForeignKey(Group)
	likers = models.ManyToManyField(User, related_name="listings")

	sold = models.BooleanField(default=False)

	def url(self): return self.BASE_URL % (self.group.id, self.id)

class Comment(models.Model):

	def __unicode__(self):
		return self.message or u'No Text'

	id = models.BigIntegerField(primary_key=True)
	message = models.TextField(null=False, blank=True, default="")
	created_time = models.DateTimeField('date published')
	user = models.ForeignKey(User)
	listing = models.ForeignKey(Listing, related_name="comments")

