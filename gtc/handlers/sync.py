# Python
import json
import datetime
import bcrypt

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


# Acts as the Frontpage when users are not signed in and the dashboard when they are.
class SyncHandler(BaseHandler):
    #we want to add all groups from datastore to a search index
    def get(self):
        #get all groups
        groups = schema.Group.fetch()

        #keep track of already indexed groups
        keys = []
        for group in groups:
            try:
                #if this is an unseen group
                if group.key not in keys:
                    keys.append(group.key)

                    #fetch the details of the group
                    taskqueue.add(
                        url='/details',
                        queue_name='fetch',
                        params={
                            'provider':   group.provider,
                            'groupid':    group.key.id()
                        }
                    )

            except Exception as e:
                print e
                pass
            continue

        self.send('OK')