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

class DisclaimerHandler(BaseHandler):

  def get(self):

    # check if we currently have that plan registered
    self.render('disclaimer.html', {

      'title':        'Disclaimer',
      'description':  'How information on this website can be used'

    }, ttl=3600)
    