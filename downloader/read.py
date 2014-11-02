from pymongo import MongoClient
from pymongo import errors
client = MongoClient()
db = client.nucraigslist
posts = db.posts

with open("posts.txt", "w") as f:
	for post in posts.find():
		message = post.get('message')
		if 'comments' in post:
			comments = post.get('comments').get('data')
		else:
			comments=""
		message = message or post.get('caption')
		if message:
			print "----------------------"
			print post.get('from').get('name') + ": " + message
			print "~~~~~~"
			for comment in comments:
				print comment.get('from').get('name') + ": " + comment.get('message')
			f.write("----------------------\n")
			f.write(message.encode('utf8', 'ignore'))
			f.write("\n~~~~~~~~~~~~~~~~~~~~~~~\n")
			for comment in comments:
				f.write(comment.get('message').encode('utf8', 'ignore'))
			f.write("\n")
