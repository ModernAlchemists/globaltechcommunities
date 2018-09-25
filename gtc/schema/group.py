# Google Libraries
from google.appengine.ext import ndb
from google.appengine.api import search

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

  def index(self):
    index = search.Index('group')
    id = self.key.id()
    doc = search.Document(
      doc_id=str(id),
      fields=[
        search.TextField(name='name', value=self.name),
        search.NumberField(name='members', value=self.members),
        search.TextField(name='slug', value=self.slug),
        search.TextField(name='description', value=strings.text_from_html(self.description)),
        search.TextField(name='image', value=self.image),
        search.TextField(name='link', value=self.link),
        search.TextField(name='provider', value=self.provider),
        search.TextField(name='uid', value=self.uid),
        search.NumberField(name='lat', value=self.lat),
        search.NumberField(name='lng', value=self.lng),
        search.TextField(name='facebook_url', value=self.facebook_url),
        search.TextField(name='facebook_uid', value=self.facebook_uid),
        search.TextField(name='meetup_url', value=self.meetup_url),
        search.TextField(name='meetup_uid', value=self.meetup_uid),
      ]
    )

    index.put(doc)

  def add_new_group(self):
    group_key = cls(
      name=self.name,          
      members=self.members,       
      slug=self.slug,          
      description=self.description,
      image=self.image,
      thumbnail=self.thumbnail,
      link=self.link,
      provider=self.provider,
      uid=self.uid,
      lat=self.lat,          
      lng=self.lng,          
      enabled=self.enabled,       
      facebook_url=self.facebook_url,  
      facebook_uid=self.facebook_uid,  
      meetup_url=self.meetup_url,    
      meetup_uid=self.meetup_uid
    )

    group_key.put()
    group_key.index()




  