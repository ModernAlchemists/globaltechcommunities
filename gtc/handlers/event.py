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
class EventHandler(BaseHandler):

  def get(self, eventid=None, slug=None):

    # get the vent
    event = schema.Event.get_by_id(long(eventid))

    # did we find it ?
    if event == None:

      # render it out
      self.send('not found')

      # nope
      return

    # save it
    event.views = event.views + 1
    event.put()

    # get the group
    group = event.group.get()

    # did we find it ?
    if group == None:

      # render it out
      self.send('not found')

      # nope
      return

    # check if we currently have that plan registered
    self.render('event.html', {

      'title': event.title,
      'event':  event,
      'group':  group,
      'background_image': group.image

    })
    