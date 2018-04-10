# Google Libraries
from google.appengine.ext import ndb

# Python Libs
import datetime
import logging
import calendar
import hashlib

# Custom Libs
from gtc.schema.base import BaseModel
import gtc.utils.string as strings

# Represents a current stage that the grid is in
class Group(BaseModel):

  # info to display about the event
  name          = ndb.StringProperty(default=None)
  members       = ndb.IntegerProperty(default=None)
  slug          = ndb.StringProperty(default=None)
  description   = ndb.TextProperty(default=None)
  image         = ndb.StringProperty(default=None)
  thumbnail     = ndb.StringProperty(default=None)
  link          = ndb.StringProperty(default=None)
  provider      = ndb.StringProperty(default=None)
  uid           = ndb.StringProperty(default=None)
  lat           = ndb.FloatProperty(default=None)
  lng           = ndb.FloatProperty(default=None)
  enabled       = ndb.BooleanProperty(default=True)

  facebook_url  = ndb.StringProperty(default=None)
  facebook_uid  = ndb.StringProperty(default=None)
  meetup_url    = ndb.StringProperty(default=None)
  meetup_uid    = ndb.StringProperty(default=None)

  # timestamps
  created       = ndb.DateTimeProperty(auto_now_add=True)
  lastupdated   = ndb.DateTimeProperty(auto_now=True)

  @staticmethod
  def get_by_uid(provider,uid):
    query = Group.query(Group.provider==provider,Group.uid==uid)
    return Group.fetch_single(query)

  @staticmethod
  def get():
    return Group.query().order(Group.name).fetch()

  @staticmethod
  def fetch():
    query = Group.query()
    query = query.order(-Group.name)
    return query.fetch()