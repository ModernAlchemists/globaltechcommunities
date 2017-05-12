# Google Libraries
from google.appengine.ext import ndb

# Python Libs
import datetime
import logging
import calendar
import hashlib

# Custom Libs
from gtc.schema.base import BaseModel
from gtc.schema.group import Group
import gtc.utils.string as strings

# Represents a current stage that the grid is in
class Event(BaseModel):

  # info to display about the event
  title         = ndb.StringProperty(default=None)
  views          = ndb.IntegerProperty(default=0)
  description   = ndb.StringProperty(default=None)
  slug          = ndb.StringProperty(default=None)
  countrycode   = ndb.StringProperty(default=None)
  country       = ndb.StringProperty(default=None)
  city          = ndb.StringProperty(default=None)
  location      = ndb.StringProperty(default=None)
  provider      = ndb.StringProperty(default=None)
  uid           = ndb.StringProperty(default=None)
  link          = ndb.StringProperty(default=None)
  lat           = ndb.FloatProperty(default=None)
  lng           = ndb.FloatProperty(default=None)
  group         = ndb.KeyProperty(kind=Group,default=None)

  # timestamps
  timestamp     = ndb.DateTimeProperty(default=None)
  created       = ndb.DateTimeProperty(auto_now_add=True)
  lastupdated   = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def get_upcoming_by_popular():
    tz = datetime.datetime.now()
    return Event.query(Event.timestamp>=tz).order(-Event.views,-Event.timestamp).fetch(limit=3)

  @staticmethod
  def get_by_uid(provider,uid):
    query = Event.query(Event.provider==provider,Event.uid==uid)
    return Event.fetch_single(query)

  @staticmethod
  def fetch():
    return Event.query().order(-Event.slug).fetch()

  @staticmethod
  def get_by_filter():
    return Event.query().order(-Event.created).fetch()

  @staticmethod
  def get_by_community(user=None):
    return Event.query(Event.created==datetime.datetime.now()).order(-Event.created).fetch()