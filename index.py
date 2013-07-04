import pymongo
import bottle
import models.Posts
import cgi
import re

#List of blog posts
@bottle.route('/')
def index():

	posts = postsModel.getPosts(10, 0)
	return bottle.template("index", {"posts": posts})

@bottle.get('/post/<permalink>')
def post(permalink):
	permalink = cgi.escape(permalink)

	post = postsModel.getPostByPermalink(permalink)

	return bottle.template("post", {"post":post})


@bottle.get('/new')
def add():

	return bottle.template("new", {"subject":"", "body":"", "tags":""})

@bottle.post('/new')
def add():

    title = bottle.request.forms.get("subject")
    post = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")

    tags = cgi.escape(tags)
    tags_array = extract_tags(tags)

    escaped_post = cgi.escape(post, quote=True)

    postsModel.insert(title, post, tags_array)

    bottle.redirect('/')

def extract_tags(tags):

    whitespace = re.compile('\s')

    nowhite = whitespace.sub("",tags)
    tags_array = nowhite.split(',')

    # let's clean it up
    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned

connection = pymongo.MongoClient('mongodb://localhost')
database = connection.blog

postsModel = models.Posts.Posts(database)


bottle.run(host='localhost',port=8082)