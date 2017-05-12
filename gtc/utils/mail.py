from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
import jinja2
import datetime

import gtc.schema as schema
import gtc.utils.string as strings

# Setup our Jinja Runner
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('emails'))

#
# Merges and returns the template vars.
# Just a quick util method
#
def __get_vars(current_vars={}):

  # current default vars
  default_vars = {
  }

  # Return merged collections
  return dict(default_vars.items() + current_vars.items())

###
# Renders a template from the email templates
###
def render(template=None,locales={}):

  # build up the environment
  locales     = __get_vars(locales)
  templ       = jinja_environment.get_template(template + '.html')

  # render the template
  templ_str   = templ.render( locales )

  # returns the created template
  return      templ_str

def send(tos=[],subject=None,html=None,text=None,template=None,locales={},signature=None):

  # params to send out
  post_params = {}

  # check if the text was given
  if text != None: 
    post_params['text']     = text
  post_params['tos']        = ','.join(tos)
  post_params['subject']    = subject
  post_params['signature']  = signature
  post_params['uid']        = (str(datetime.datetime.now()) + strings.random(32)).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')

  # set the mail uid
  locales['uid']            = post_params['uid'] 

  # check if the template was given ?
  if template != None:

    # render the template with vars
    html = render(template=template, locales=locales)

    # set the html
    post_params['html'] = html

  else:

    # set the html
    post_params['html'] = html

  # recursive back to us
  """
  taskqueue.add(
  
    url='/tasks/mail',
    queue_name='emails',
    params=post_params

  )
  """