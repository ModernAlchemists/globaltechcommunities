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

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class EventsHandler(BaseHandler):

  def get(self):

    # get the events
    events = schema.Event.get_by_filter()

    # the final item list
    items = []

    # list them all
    for event in events:

      # add it
      items.append({

        'event':  event,
        'group':  event.group.get()

      })

    # check if we currently have that plan registered
    self.render('events.html', {

      'title': 'Events',
      'items': items,
      'background_image': '/img/photos/techtalkcptjune160127.jpg'

    })
    