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

  @classmethod
  def add_new_group(cls,name,members,slug,description,image,thumbnail,link,provider,uid,lat,lng,enabled,facebook_url,facebook_uid,meetup_url,meetup_uid):
    group_key = cls(
      name=name,          
      members=members,       
      slug=slug,          
      description=description,
      image=image,
      thumbnail=thumbnail,
      link=link,
      provider=provider,
      uid=uid,
      lat=lat,          
      lng=lng,          
      enabled=enabled,       
      facebook_url=facebook_url,  
      facebook_uid=facebook_uid,  
      meetup_url=meetup_url,    
      meetup_uid=meetup_uid
    ).put()

    index = search.Index('group')
    doc = search.Document(
      doc_id=str(group_key.id()),
      fields=[
        search.TextField(name='name',value=name),
        search.NumberField(name='members',value=members),
        search.TextField(name='slug',value=slug),
        search.TextField(name='description',value=description),
        search.TextField(name='image',value=image),
        search.TextField(name='link',value=link),
        search.TextField(name='provider',value=provider),
        search.TextField(name='uid',value=uid),
        search.NumberField(name='lat',value=lat),
        search.NumberField(name='lng',value=lng),
        search.TextField(name='facebook_url',value=facebook_url),
        search.TextField(name='facebook_uid',value=facebook_uid),
        search.TextField(name='meetup_url',value=meetup_url),
        search.TextField(name='meetup_uid',value=meetup_uid)
      ]
    )

    index.put(doc)

  