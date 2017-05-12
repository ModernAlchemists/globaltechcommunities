# Google Libraries
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.api import images

# Python Libs
import datetime
import logging

#
# Base Model for all our types
# @author Johann du Toit
#
class BaseModel(ndb.Model):
	
	@staticmethod
	def fetch_single(query_obj):

		# Get all the accounts with that limit
		item_objs = query_obj.fetch(limit=1)

		# Did we get a account ?
		if item_objs != None and len(item_objs) > 0:

			# Return the first
			return item_objs[0]

		else: return None