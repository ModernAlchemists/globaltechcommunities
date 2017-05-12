# Python
import json
import datetime
import time
import bcrypt

# Google Apis
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.api import urlfetch

# Custom importing
from base import BaseHandler
import gtc.utils.log as log
import gtc.utils.string as strings
import gtc.schema as schema
import gtc.constants as constants

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class DetailsHandler(BaseHandler):

  # Renders the dashboard of the user
  def get(self): self.redirect('/')
  def post(self):
    provider  = self.request.POST.get('provider')
    groupid   = self.request.POST.get('groupid')

    group = schema.Group.get_by_id(long(groupid))
    if group == None:
      self.send('not found')
      return

    result = urlfetch.fetch(

      url='https://api.meetup.com/' + str(group.slug) + '?member_id=' + str(constants.MEETUP_MEMBER_ID) + '&key=' + str(constants.MEETUP_API_TOKEN) + '&page_start=0',
      validate_certificate=False,
      follow_redirects=True,
      deadline=10,
      allow_truncated=True

    )

    if result.status_code == 200:
      body = None
      try:
        body = json.loads(result.content)
      except Exception as e:
        pass

      if body == None:
        self.response.out.write('NOPE')
        return

      group.lat = float(body['lat'])
      group.lng = float(body['lon'])
      group.members = int(body['members'])
      group.description = body['description']
      if 'key_photo' in body:
        group.image = body['key_photo']['highres_link']
      if 'key_photo' in body:
        group.thumbnail = body['key_photo']['photo_link']
      group.put()
    self.send('done')
    