from pymongo import MongoClient
from pymongo import errors
client = MongoClient()
db = client.nucraigslist
posts = db.posts

with open("posts.txt", "w") as f:
	for post in posts.find():
		message = post.get('message')
		message = message or post.get('caption')
		if message:
			print "----------------------"
			print message
			f.write("----------------------\n")
			f.write(message.encode('utf8', 'ignore'))
			f.write("\n")
