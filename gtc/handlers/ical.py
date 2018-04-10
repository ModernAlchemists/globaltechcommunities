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


def limit_to_75_octets(inp):
  if len(inp) <= 73:
    return inp + "\r\n"

  out = ""
  while len(inp) > 73:
    out += inp[:73] + "\r\n"
    inp = " " + inp[73:]

  if len(inp) == 0:
    return out
  else:
    return out + inp + "\r\n"

def render_alarm():
  return ("BEGIN:VALARM\r\n" +
    "TRIGGER:-PT10M\r\n" +
    "ACTION:DISPLAY\r\n" +
    limit_to_75_octets("DESCRIPTION:Reminder: %s" % DESC) +
    "END:VALARM\r\n")

def render_event(event):
  """create and event
  uid: unique event id
  dtstamp: time when event was created
  dtstart: event start time
  dtend: event end time (all dates are in utc)
  """
  return ("BEGIN:VEVENT\r\n" +
    "UID:" + limit_to_75_octets(event.provider + '' + event.uid) + "\r\n" +
    "DTSTAMP:20141107T200200Z\r\n" +
    "DTSTART:20141109T153000Z\r\n" +
    "DTEND:20141109T163000Z\r\n" +
    limit_to_75_octets("SUMMARY:%s" % event.title) +
    # render_alarm() +
    "END:VEVENT\r\n")

def render_events(events):
  ev = []
  for event in events: ev.append(render_event(event))
  return ''.join(ev)

def render_calendar(events):
  return ("BEGIN:VCALENDAR\r\n" +
    "VERSION:2.0\r\n" +
    "PRODID:-//Global Tech Communities.//CalDAV Server//EN\r\n" +
    render_events(events) +
    "END:VCALENDAR\r\n")

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class GroupICalHandler(BaseHandler):

  def get(self, communityid=None):

    # get the vent
    group = schema.Group.get_by_id(long(communityid))

    # did we find it ?
    if group == None:

      # render it out
      self.send('not found')

      # nope
      return

    # get the current year
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    # get the dates
    _, num_days = calendar.monthrange(int(year), int(month))

    # get the range
    starts  = datetime.datetime(int(year), int(month), 1, 0, 0)
    ends    = datetime.datetime(int(year), int(month), num_days, 0, 0)

    # get the events
    events = schema.Event.get_by_filter(

      starts=starts,
      ends=ends,
      group=group

    )

    self.response.headers['content-type'] = 'Content-type: text/calendar; charset=utf-8'
    self.response.headers['content-disposition'] = 'inline; filename=calendar.ics'

    # send it out
    self.send(render_calendar(events))

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class GlobalICalHandler(BaseHandler):

  def get(self):

    # get the current year
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

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

    self.response.headers['content-type'] = 'Content-type: text/calendar; charset=utf-8'
    self.response.headers['content-disposition'] = 'inline; filename=calendar.ics'

    # send it out
    self.send(render_calendar(events))
    