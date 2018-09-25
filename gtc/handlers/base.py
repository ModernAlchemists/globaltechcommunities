# Google Apis
from google.appengine.api import users
from google.appengine.api.logservice import logservice
from google.appengine.api import memcache
from webapp2_extras import sessions
import webapp2
import jinja2

# Python Apis
import os
import re
import json
import time
import logging
from datetime import date

# Local libs
import gtc.schema as schema
import gtc.utils.string as string_utils

# Setup our Jinja Runner
jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader('views'),
  autoescape=True
)

CURRENT_VERSION = string_utils.md5(os.environ['CURRENT_VERSION_ID'])

#
# Acts as the Frontpage when users are not signed in and the dashboard when they are
#
class BaseHandler(webapp2.RequestHandler):

  # Has not run !
  has_setup_run = False

  #
  # Returns if we are in production
  def is_production(self): return not os.environ['SERVER_SOFTWARE'].lower().startswith('dev')
  
  # Return True or False
  # wether the user is logged in
  # or not
  def is_logged_in(self):

    # Just a quick return
    return 'logged_in_user_id' in self.session and self.session['logged_in_user_id'] != None

  # Return True or False
  # wether the user is logged in
  # or not
  def set_logged_in_userid(self, userid):
    
    # set it
    self.session['logged_in_user_id'] = userid

  # Return True or False
  # wether the user is logged in
  # or not
  def get_logged_in_user(self):

    if self.is_logged_in() == False:

      # nope
      return None

    # Just a quick return
    return schema.User.get_by_id(long(self.session['logged_in_user_id']))

  # Return True or False
  # wether the user is logged in
  # or not
  def get_logged_in_userid(self):

    if self.is_logged_in() == False:

      # nope
      return None

    # Just a quick return
    return self.session['logged_in_user_id']

  #
  # Render the 404 error page
  #
  def renderError(self, status=404):

    # get the format
    output_format = self.get_format()

    # set the response
    self.response.status = status

    # if json output json
    if(output_format == 'json'):

      # output json
      self.send(json.dumps({

        'message': 'No such module was found'

      }))

    else:

      # render the homepage
      self.render('notfound.html', {

        'title': 'Page not Found',
        'description': 'The requested page was not found'

      })

  # Return True or False
  # wether the user is logged in
  # or not
  def is_logged_in_number(self):

    # Just a quick return
    return 'logged_in_number' in self.session and self.session['logged_in_number'] != None

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self.session_store.get_session()

  def setup(self):

    # Run setup if not already run !
    if self.has_setup_run is False:

      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)

      # Flag that setup has run !
      self.has_setup_run = True
 
  # Do some general checks
  # here we mostly just check users
  def dispatch(self):
    print 'dispatch'
    print "URL: " + str(self.request.path)

    # Run the setup
    self.setup()

    try:

      # Set headers we might want
      self.response.headers['x-frame-options'] = 'SAMEORIGIN'
      self.response.headers['x-content-type-options'] = 'nosniff'
      self.response.headers['x-xss-protection'] = '1; mode=block'
      self.response.headers['x-ua-compatible'] = 'IE=10,chrome=1'

      # check for a cached version
      page_key_str = str(os.environ['CURRENT_VERSION_ID']) + '-site-page-' + str( self.request.path )

      # just render if this page is cached
      cached_template_str = memcache.get(page_key_str)

      # done
      if cached_template_str is None or self.is_production() == False:

        # Right carry on
        super(BaseHandler, self).dispatch()

      else: 
        self.response.out.write(cached_template_str)
  
    finally:

      # Save all sessions changes
      self.session_store.save_sessions(self.response)

  # Our global key to check for if
  # a site comes in
  viewing_site_key = None

  # Our defaults
  defaults = {

    'title': False,
    'description': False,
    'keywords': False,
    'author': False,
    'errors': [],
    'config': os.environ,
    'current_year': date.today().year,
    'background_image': False,
    'current_version': CURRENT_VERSION

  }

  #
  # Merges and returns the template vars.
  # Just a quick util method
  #
  def get_default_template_vars(self, current_vars={}):

    # current default vars
    default_vars = self.defaults

    # Check if production
    is_production = self.is_production()

    # Set posted items
    post_params = {}
    for key in self.request.POST.keys():

      # Set by key
      post_params[key] = self.request.POST.get(key)

    # Set as view option
    default_vars['post_params'] = post_params

    # give the views information on if we are live ...
    default_vars['is_production'] = is_production

    # is there a current logged in number ?
    if self.is_logged_in():
      default_vars['logged_in_userid'] = self.get_logged_in_userid()
    else: 
      default_vars['logged_in_userid'] = False

    # Add logged in user details if saved in session
    if 'logged_in_user_id' in self.session and self.session['logged_in_user_id'] != None:

      # Set our logged in user to use for the view
      default_vars['logged_in_user'] = schema.User.get_by_id( long( self.session['logged_in_user_id'] ) )

    else:

      # False user !
      default_vars['logged_in_user'] = False

    # Return merged collections
    return dict(default_vars.items() + current_vars.items())

  # returns the response type requested
  def get_format(self): return self.request.path.split('.')[-1]

  # Wrapper for output
  def send(self, output_str): self.response.out.write(output_str)

  #
  # Quick definition wrapper to output the sent template
  #
  def render(self, template_str, template_vars=None, ttl=None):

    # build up the environment
    template_vars = self.get_default_template_vars(template_vars)
    template = jinja_environment.get_template(template_str)

    # render the template
    template_str = template.render( template_vars )

    # minify it
    template_str = re.sub(r'>\s+<', '><', template_str)

    # check for a cached version
    page_key_str = str(os.environ['CURRENT_VERSION_ID']) + '-site-page-' + str( self.request.path )

    # cache if requested
    if ttl != None and self.is_logged_in() == False:
      memcache.add(key=page_key_str, value=template_str, time=ttl)

    # output the page
    self.response.out.write(template_str)
  