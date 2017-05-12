# Python
import json
import datetime
import time
import httplib

# Google Apis
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from google.appengine.api.logservice import logservice
from webapp2_extras import sessions
from google.appengine.api import urlfetch

# Custom importing
from cron.handlers.base import BaseHandler
import cron.schema as schema
import cron.utils.string as strings
import cron.constants as constants

# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class MailHandler(BaseHandler):
  def post(self):

    # params
    uid         = self.request.POST.get('uid')
    signature   = self.request.POST.get('signature')
    emails      = self.request.POST.get('tos')
    subject     = self.request.POST.get('subject')
    html        = self.request.POST.get('html')
    text        = self.request.POST.get('text')

    # was job id given ?
    if strings.is_empty(uid) == True:
      print "uid required"
      self.send('uid is required')
      return

    # was job id given ?
    if strings.is_empty(emails) == True:
      print "TOS required"
      self.send('TOS is required')
      return

    # was job id given ?
    if strings.is_empty(subject) == True:
      print "SUBJECT required"
      self.send('Subject is required')
      return

    # was job id given ?
    if strings.is_empty(html) == True:
      print "HTML required"
      self.send('HTML is required')
      return

    # emails to send
    targets = []
    tos     = emails.split(',')

    # loop the emails
    for to in tos: targets.append({

      'email': str(to).strip()

    })

    # was job id given ?
    if len(targets) == 0:
      print "TOS required"
      self.send('tos is 0 length')
      return

    # do the actual request
    result = urlfetch.fetch(

      url='https://api.sendgrid.com/v3/mail/send',
      headers={

        'Authorization':  'Bearer ' + str(constants.SENDGRID_TOKEN),
        'Content-Type':   'application/json'

      },
      method='POST',
      validate_certificate=False,
      follow_redirects=True,
      deadline=10,
      allow_truncated=True,
      payload=json.dumps({
        "personalizations": [
          {
            "to":       targets,
            "subject":  subject
          }
        ],
        "from": {
          "email":      constants.SENDGRID_FROM
        },
        "content": [
          {
            "type":     "text/plain",
            "value":    str(text)
          },
          {
            "type":     "text/html",
            "value":    str(html)
          }
        ]
      })

    )

    # send out the actual mail
    self.send('OK')