# Python
import json
import datetime
import time
import bcrypt

# Google Apis
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions

# Custom importing
from base import BaseHandler
import gtc.utils.log as log
import gtc.utils.string as strings
import gtc.schema as schema
import gtc.constants as constants

from datetime import timedelta, tzinfo

class FixedOffset(tzinfo):
  """Fixed offset in minutes: `time = utc_time + utc_offset`."""
  def __init__(self, offset):
    self.__offset = timedelta(minutes=offset)
    hours, minutes = divmod(offset, 60)
    #NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
    #  that have the opposite sign in the name;
    #  the corresponding numeric value is not used e.g., no minutes
    self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)
  def utcoffset(self, dt=None):
    return self.__offset
  def tzname(self, dt=None):
    return self.__name
  def dst(self, dt=None):
    return timedelta(0)
  def __repr__(self):
    return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class FetchHandler(BaseHandler):

  # Renders the dashboard of the user
  def get(self):

    # providers = [ 'meetup', 'facebook' ]
    providers = [ 'meetup', 'facebook' ]
    for provider in providers:
      taskqueue.add(
      
        url='/fetch',
        queue_name='fetch',
        params={
          
          'provider':   provider

        }

      )
    self.response.out.write('OK')

  def post(self):
    provider = self.request.POST.get('provider')

    if provider == 'facebook': 

      # get the group uid
      group_id = self.request.POST.get('groupid')

      # is this for a group .. ?
      if group_id != None and group_id != False:

        # get the group
        group = schema.Group.get_by_id(long(group_id))

        if group == None:
          print "Group not found"
          return

        print 'https://graph.facebook.com/' + group.facebook_uid + '/events?access_token=796452663852382|a6d55adb3e9fb4e5ed53bb018b9296e1'

        result = urlfetch.fetch(

          url='https://graph.facebook.com/' + group.facebook_uid + '/events?access_token=796452663852382|a6d55adb3e9fb4e5ed53bb018b9296e1',
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

          keys = []
          if 'data' in body:
            for item in body['data']:

              event = schema.Event.get_by_uid(provider,str(item['id']))
              if event == None:
                event = schema.Event()

              date_str = item["start_time"]
              naive_date_str = date_str[0:-5]
              offset_str = date_str[-5::]

              naive_dt = datetime.datetime.strptime(naive_date_str, '%Y-%m-%dT%H:%M:%S')
              offset = int(offset_str[-4:-2])*60 + int(offset_str[-2:])
              if offset_str[0] == "-":
                 offset = -offset

              event.timestamp = naive_dt
              event.title = item['name']

              # must have a venue ...
              if 'place' in item and 'location' in item['place']:
                event.location = item['place']['location']['street']
                event.city = str(item['place']['location']['city']).lower()
                event.lat = float(item['place']['location']['latitude'])
                event.lng = float(item['place']['location']['longitude'])
                event.countrycode = str(item['place']['location']['country']).lower()
                event.country = str(item['place']['location']['country']).lower()

              event.group = group.key
              event.slug = strings.slugify(item['name'])

              # check if not already in list ...
              registered_event = schema.Event.get_by_slug(provider, event.slug)
              if registered_event != None: continue

              if 'description' in item:
                event.description = item['description']

              event.link = group.facebook_url
              event.provider = provider
              event.uid = str(item['id'])
              event.put()

          self.response.out.write('DONE')

        else:
          self.response.out.write('NOPE')
      else:
        groups = schema.Group.fetch()
        for group in groups:
          if group.facebook_uid != None and group.facebook_uid != 'None':
            taskqueue.add(
        
              url='/fetch',
              queue_name='fetch',
              params={
                
                'provider':   provider,
                'groupid':    group.key.id()

              }

            )
        self.send("DONE")

    elif provider == 'meetup':
      result = urlfetch.fetch(

        url='https://api.meetup.com/self/calendar?member_id=' + str(constants.MEETUP_MEMBER_ID) + '&key=' + str(constants.MEETUP_API_TOKEN) + '&page_start=0',
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

        keys = []
        for item in body:

          group = schema.Group.get_by_uid(provider,str(item['group']['id']))
          if group == None:
            group = schema.Group()
          group.slug = item['group']['urlname']
          group.name = item['group']['name']
          group.link = 'https://www.meetup.com/' + item['group']['urlname']
          group.provider = provider
          group.uid = str(item['group']['id'])

          group.put()

          if group.key not in keys:
            taskqueue.add(
      
              url='/details',
              queue_name='fetch',
              params={
                
                'provider':   provider,
                'groupid':    group.key.id()

              }

            )

          keys.append(group.key)

          event = schema.Event.get_by_uid(provider,str(item['id']))
          if event == None:
            event = schema.Event()
          event.timestamp = datetime.datetime.fromtimestamp( long(item['time']) / 1e3 )
          event.title = item['name']

          # must have a venue ...
          if 'venue' in item:
            event.location = item['venue']['address_1']
            event.city = str(item['venue']['city']).lower()
            event.lat = float(item['venue']['lat'])
            event.lng = float(item['venue']['lon'])
            event.countrycode = str(item['venue']['country']).lower()
            event.country = str(item['venue']['localized_country_name']).lower()

          event.group = group.key
          event.slug = strings.slugify(item['name'])

          # check if not already in list ...
          registered_event = schema.Event.get_by_slug(provider, event.slug)
          if registered_event != None: continue

          if 'description' in item:
            event.description = item['description']

          event.link = item['link']
          event.provider = provider
          event.uid = str(item['id'])
          event.put()

        self.response.out.write('DONE')

      else:
        self.response.out.write('NOPE')

    else:
      self.response.out.write('NOPE')
    