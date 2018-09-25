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
class CommunityHandler(BaseHandler):

  def get(self, communityid=None, slug=None):

    # get the vent
    group = schema.Group.get_by_id(long(communityid))
    print 'looking for %s ' % communityid
    # did we find it ?
    if group == None:

      # render it out
      self.send('not found')

      # nope
      return

    # the start date
    timestamp = datetime.datetime.now()

    # get the events
    events = schema.Event.get_by_filter(starts=timestamp,group=group,limit=3)

    # check if we currently have that plan registered
    self.render('community.html', {

      'title': group.name,
      'group': group,
      'events': events,
      'background_image': group.image

    }, ttl=3600)


    