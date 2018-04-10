# Python
import json
import datetime
import bcrypt

# Google Apis
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Custom importing
from gtc.handlers.base import BaseHandler
import gtc.utils.log as log
import gtc.utils.string as strings
import gtc.schema as schema

class FAQHandler(BaseHandler):

  def get(self):

    # check if we currently have that plan registered
    self.render('faq.html', {

      'title':        'Frequently Asked Questions',
      'description':  'Answers to questions we see quite'

    }, ttl=3600)
    