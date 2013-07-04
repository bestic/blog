import pymongo
import datetime
import re

class Posts:
	
	def __init__(self, db):
		self.db = db
		self.posts = db.posts

	def insert(self, title, post, tags):

		exp = re.compile('\W') # match anything not alphanumeric
		whitespace = re.compile('\s')
		temp_title = whitespace.sub("_",title)
		permalink = exp.sub('', temp_title)

		# Build a new post
		post = {"title": title,
				"body": post,
				"permalink":permalink,
				"tags": tags,
				"comments": [],
				"date": datetime.datetime.utcnow()}

		# now insert the post
		try:
			self.posts.insert(post)
			print "Inserting the post"
		except:
			print "Error inserting post"
			print "Unexpected error:", sys.exc_info()[0]

		return permalink


	def getPosts(self, num, skip):

		return self.posts.find().sort('date_added', pymongo.DESCENDING).skip(skip).limit(num)


	def getPostByPermalink(self, permalink):

		return self.posts.find_one({'permalink':permalink})


