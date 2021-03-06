import logging

from datetime import datetime
from calendar import timegm

from google.appengine.ext import db

from models.user import User

class Idea(db.Model):
	title = db.StringProperty(required=True)
	author = db.ReferenceProperty(User, required=True, collection_name="ideaAuthor")
	answers = db.StringListProperty(required=True)
	version = db.StringProperty(required=True)
	positive = db.IntegerProperty(required=True, default=0)
	negative = db.IntegerProperty(required=True, default=0)
	comments = db.IntegerProperty(required=True, default=0)
	score = db.FloatProperty(required=True, default=0.0)
	country = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)

	@staticmethod
	def get_current_version():
		return "1"

	@staticmethod
	def get_steps(version):
		steps = []
		
		if(version == "1"):
			steps = [{
				"slug": "problem",
				"title": "Problem",
				"question": "What problem are you trying to solve? Who has it?",
			},{
				"slug": "solution",
				"title": "Solution",
				"question": "What are you going to build?",
			},{
				"slug": "acquisition",
				"title": "Acquisition",
				"question": "How will you attract potential users/customers?",
			},{
				"slug": "business_model",
				"title": "Business Model",
				"question": "How are you going to make money?",
			},{
				"slug": "competitors",
				"title": "Competitors",
				"question": "Who will you compete with?",
			},{
				"slug": "milestones",
				"title": "Milestones",
				"question": "Are you posting this idea for fun? To find a cofounder? Get Feedback? Please, tell where you are.",
			}]			
		else:
			logging.error("Idea version does not exist...")
		
		return steps
	
	@staticmethod
	def get_current_steps():
		return Idea.get_steps(Idea.get_current_version())
	
	@staticmethod
	def get_extended_idea(idea):
		extended_steps = []
		steps = Idea.get_steps(idea.version)

		for i in range(len(steps)):
			title = steps[i]["title"]
			question = steps[i]["question"]
			slug = steps[i]["slug"]
			answer = idea.answers[i]

			extended_steps.append({
				"title": title,
				"question": question,
				"slug": slug,
				"answer": answer,
			})
			
		extended_idea = {
			"id": idea.key().id(),
			"title": idea.title,
			"positive": idea.positive,
			"negative": idea.negative,
			"comments": idea.comments,
			"created": idea.created,
			"extended_steps": extended_steps,
		}
		
		return extended_idea
	
	@staticmethod
	def validate(request, idea=None):
		validated = True
		
		answers = []
		title = request.get("title")
	
		if title == "":
			validated = False
		else:	
			logging.info("Title: %s" % (title)) 
			
			steps = Idea.get_current_steps()
			if idea:
				steps = Idea.get_steps(idea.version)
			
			for step in steps:
				attribute = "answer_" + step["slug"]
				answer = request.get(attribute)

				if answer and len(answer) <= 140:
					answers.append(answer)
				else:
					validated = False
					break
		
		return validated, title, answers

	@staticmethod
	def get_last_ideas(user=None, country=None, offset=None):
		if offset:
			offset_timestamp = datetime.utcfromtimestamp(int(offset))

		size=50
		q = Idea.all()

		if(user):
			q.filter("author = ", user.key())

		if(country):
			q.filter("country = ", country.upper())

		if offset:
			q.filter("created <", datetime.utcfromtimestamp(int(offset)))

		q.order("-created")

		ideas = q.fetch(size+1)

		new_offset = None
		if(len(ideas)==size+1):
			last_idea = ideas[len(ideas)-2]
			new_offset = timegm(last_idea.created.utctimetuple())
			del ideas[-1]

		return ideas, new_offset






				
		
		
		
			
		
		
	
