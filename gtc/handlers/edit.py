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
class AdminGroupEditHandler(BaseHandler):

  def post(self, communityid=None):

    # get the vent
    group = schema.Group.get_by_id(long(communityid))

    # did we find it ?
    if group == None:

      # render it out
      self.send('not found')

      # nope
      return

    # get the params
    param_facebook_url    = self.request.POST.get('facebook_url')
    param_facebook_uid    = self.request.POST.get('facebook_uid')
    param_meetup_url      = self.request.POST.get('meetup_url')
    param_meetup_uid      = self.request.POST.get('meetup_uid')

    param_name            = self.request.POST.get('name')
    param_desc            = self.request.POST.get('description')

    # set it
    group.name          = param_name
    group.description   = param_desc

    # set the group details
    group.facebook_url  = param_facebook_url
    group.facebook_uid  = param_facebook_uid

    # set the meetup update
    group.meetup_url    = param_meetup_url
    group.meetup_uid    = param_meetup_uid

    # save it
    group.put()

    # check if we currently have that plan registered
    self.render('edit.html', {

      'title': group.name,
      'group': group,
      'background_image': group.image

    }, ttl=3600)

  def get(self, communityid=None):

    # get the vent
    group = schema.Group.get_by_id(long(communityid))

    # did we find it ?
    if group == None:

      # render it out
      self.send('not found')

      # nope
      return

    # check if we currently have that plan registered
    self.render('edit.html', {

      'title': group.name,
      'group': group,
      'background_image': group.image

    }, ttl=3600)
    