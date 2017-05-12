from google.appengine.ext import vendor
import os

# Add any libraries installed in the "lib" folder.
# vendor.add('lib')

if os.environ.get('SERVER_SOFTWARE', '').lower().startswith('development'):
  remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = ('REMOTE_ADDR', ['127.0.0.1'])