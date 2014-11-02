from django.db import models

class User(models.Model):

	def __unicode__(self):
		return self.name

	name = models.CharField(max_length = 20)
	uid = models.BigIntegerField()

class Listing(models.Model):

	def __unicode__(self):
		return self.listing_text

	listing_text = models.CharField(max_length = 400)
	pub_date = models.DateTimeField('date publshed')
	seller = models.ForeignKey(User)
	approved = models.BooleanField(default=False)
	buy_or_sell = models.CharField(max_length = 4, null=True)
	category = models.CharField(max_length=15, null=True)

class Comment(models.Model):

	def __unicode__(self):
		return self.comment_text

	comment_text = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date published')
	user = models.ForeignKey(User)
	listing = models.ForeignKey(Listing)

