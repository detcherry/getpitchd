from google.appengine.ext import db

class User(db.Model):
	twitter_id = db.StringProperty(required = True)
	twitter_access_token_key = db.StringProperty(required = True)
	twitter_access_token_secret = db.StringProperty(required = True)
	username = db.StringProperty(required = True)
	name = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)