# Python
import json
import datetime
import bcrypt
import calendar

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
class EventsListOutputHandler(BaseHandler):

  def get(self, year=None, month=None):

    # get the dates
    _, num_days = calendar.monthrange(int(year), int(month))

    # get the range
    starts  = datetime.datetime(int(year), int(month), 1, 0, 0)
    ends    = datetime.datetime(int(year), int(month), num_days, 0, 0)

    # get the events
    events = schema.Event.get_by_filter(

      starts=starts,
      ends=ends

    )

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class EventsListHandler(BaseHandler):

  def get(self, year=None, month=None):

    # get the current year
    current_year = datetime.datetime.now().year

    # check the item
    if len(str(year)) != 4 or len(str(month)) != 2:

      # redirect it away
      self.redirect('/' + '/'.join([

        'events',
        str(year).zfill(4),
        str(month).zfill(2)

      ]))

      # done
      return

    # is this bigger than 12 or 13
    if int(month) > 12 or int(month) < 1:
      self.redirect('/events')
      return

    # check the year
    if int(year) > current_year or int(year) < 2017:
      self.redirect('/events')
      return

    # get the dates
    _, num_days = calendar.monthrange(int(year), int(month))

    # get the date
    dt = datetime.datetime.now()
    starting_day = 1
    if int(month) == int(dt.month):
      starting_day = dt.day

    # get the range
    starts  = datetime.datetime(int(year), int(month), starting_day, 0, 0)
    ends    = datetime.datetime(int(year), int(month), num_days, 0, 0)

    # get the events
    events = schema.Event.get_by_filter(

      starts=starts,
      ends=ends

    )

    # the final item list
    items = []
    entries = []

    # list them all
    for event in events:

      # get the group
      group = event.group.get()

      # check if it has a location ..
      if event.location == None: continue
      if event.city == None: continue
      if event.country == None: continue

      # set the title
      title = None

      try:
        # set the title
        title = str(event.title)

        if event.city != None:
          title = str(event.city).upper() + ' - ' + title
      except Exception as e:
        title = None

      # did we find it ?
      if title == None: continue

      # add to the list
      entries.append({

        'title': title,
        'className': 'bg-red',
        'link': '/' + '/'.join([

          'events',
          str(year).zfill(4),
          str(month).zfill(2),
          str(event.key.id())

        ]),
        'start': str(datetime.datetime(

          event.timestamp.year, 
          event.timestamp.month, 
          event.timestamp.day, 

          event.timestamp.time().hour, 
          event.timestamp.time().minute

        )),
        'end': str(datetime.datetime(

          event.timestamp.year, 
          event.timestamp.month, 
          event.timestamp.day, 

          1, 
          0

        ))

      })

    # check if we currently have that plan registered
    self.render('events.html', {

      'title': 'Events',
      'year': str(year),
      'month': str(month),
      'entries': entries,
      'background_image': '/img/photos/techtalkcptjune160127.jpg'

    },ttl=3600)

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class EventsHandler(BaseHandler):

  def get(self):

    # get the date
    timestamp = datetime.datetime.now()

    # redirect to the current year
    self.redirect('/' + '/'.join([

      'events',
      str(timestamp.year).zfill(4),
      str(timestamp.month).zfill(2)

    ]))
    