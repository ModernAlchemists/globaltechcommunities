#!/usr/bin/env python

# Python Libs
import os
import sys
import urllib

# Google Apis
import webapp2
from webapp2_extras import routes

from gtc.handlers.home import HomeHandler
from gtc.handlers.fetch import FetchHandler
from gtc.handlers.details import DetailsHandler

from gtc.handlers.events import EventsHandler
from gtc.handlers.event import EventHandler

from gtc.handlers.communities import CommunitiesHandler
from gtc.handlers.community import CommunityHandler

from gtc.handlers.sponsor import SponsorHandler, SponsorFormHandler
from gtc.handlers.contact import ContactFormHandler, ContactHandler

# General Config for our web application
config = {
  
  'webapp2_extras.sessions': {

    'secret_key': os.environ['SESSION_SECRET'],
    'cookie_args': {

      'max_age': 60 * 60 * 24 * 31 * 12

    }

  }

}

# handle the routes
route_objs = [
  
  ('/', HomeHandler),

  ('/fetch', FetchHandler),
  ('/details', DetailsHandler),

  ('/events', EventsHandler),
  webapp2.Route('/events/<eventid:[\d]+>', EventHandler),
  webapp2.Route('/events/<eventid:[\d]+>/<slug:[.*]+>', EventHandler),
  ('/communities', CommunitiesHandler),
  webapp2.Route('/communities/<communityid:[\d]+>', CommunityHandler),
  webapp2.Route('/communities/<communityid:[\d]+>/<slug:[.*]+>', CommunityHandler),

  ('/sponsor', SponsorHandler),
  ('/sponsorship-form', SponsorFormHandler),

  ('/contact', ContactHandler),
  ('/contactus', ContactFormHandler)

  # webapp2.Route('/jobs/<jobid:[\d]+>/history/<requestid:[\d]+>', RequestHandler),
  # webapp2.Route(r'/<:.*>', NotFoundHandler)

]

# Startup our app with the routes we are going to configure now
app = webapp2.WSGIApplication(

  route_objs, 
  debug=os.environ['SERVER_SOFTWARE'].lower().startswith('dev'), 
  config=config

)