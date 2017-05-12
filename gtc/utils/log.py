from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
import jinja2
import datetime

import gtc.schema as schema
import gtc.utils.string as strings

def send(message):

  # recursive back to us
  taskqueue.add(
  
    url='/tasks/log',
    queue_name='log',
    params={

      'message': message

    }

  )