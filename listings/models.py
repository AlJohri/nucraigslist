from django.db import models

class User(models.Model):

	def __unicode__(self):
		return self.name

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length = 20)

class Listing(models.Model):

	BASE_URL = "https://www.facebook.com/357858834261047/posts/"

	def __unicode__(self):
		return self.message or u'No Text'

	id = models.BigIntegerField(primary_key=True)
	created_time = models.DateTimeField(null=False)
	updated_time = models.DateTimeField(null=False)
	type = models.CharField(max_length=6)
	message = models.CharField(max_length = 400, null=False, blank=True, default="")

	parsed = models.BooleanField(default=False)
	seller = models.ForeignKey(User)
	approved = models.BooleanField(default=False)
	buy_or_sell = models.CharField(max_length = 4, null=True)
	category = models.CharField(max_length=15, null=True)

	def url(self):
		return self.BASE_URL + self.id

class Comment(models.Model):

	def __unicode__(self):
		return self.comment_text or u'No Text'

	comment_text = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date published')
	user = models.ForeignKey(User)
	listing = models.ForeignKey(Listing)

