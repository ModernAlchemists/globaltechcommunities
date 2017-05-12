# -*- coding: utf-8 -*-
import re
import string
import random as rn
import hashlib

#
# Returns all numeric characters in the string
#
def is_number(text):
  numb = to_number(text)
  return (numb != None, numb)

#
# Returns all numeric characters in the string
#
def to_number(text):

  # set the price
  parsing_str = str( text ).strip()

  # get all the numbers
  parsing_strs = re.findall(r'[\.\d]+', parsing_str)

  # did we find any ?
  if parsing_strs != None:

    # set the price
    try:
      return float( ''.join(parsing_strs) )
    except Exception, e:

      try:
        return int( ''.join(parsing_strs) )
      except Exception, e:
        pass

  # return that we didn't find any numbers ...
  return False

#
# Checks if empty
#
def is_empty(str_to_check=None):
  if str_to_check == None: return True
  if str_to_check == False: return True
  if str_to_check == "": return True
  if str(str_to_check).strip() == "": return True
  return False

#
# String to hash with md5
#
def md5(str_to_hash):

  if is_empty(str_to_hash): 
    return None

  m = hashlib.md5()
  m.update(str_to_hash)
  return m.hexdigest()

# 
# Returns a random string
#
def random(size=6):
  return ''.join(rn.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') for x in range(size))

#
# Returns the slug of a string
#
def slugify(text_str):
  text_str = str( unicode(text_str).encode('ascii', 'ignore') ).strip().lower()
  return re.sub(r'\W+','-',text_str)