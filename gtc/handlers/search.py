#Google Apis
from google.appengine.api import search

# Custom importing
from gtc.handlers.base import BaseHandler
import gtc.schema as schema

#python
from jinja2 import utils
from cgi import parse_qs
import string
import urllib
from urlparse import urlparse
import re
from random import randint

class SearchHandler(BaseHandler):

  def get(self):
    # search_term = str(utils.escape(self.request.get('q')))
    uri = urlparse(self.request.uri)

    if uri.query:
        # get our query
        search_term = parse_qs(uri.query)
        query_length = len(search_term)
        if query_length < 1:
            self.redirect('/')
            return 
        
        search_term = search_term['q'][0].strip() #remove spaces and tabs

        #get ready to build expression for search
        expr = []
        # #add ascending sort to expression
        expr.append(search.SortExpression(
            expression='name', default_value = '',
            direction=search.SortExpression.ASCENDING
        ))

        #build search options
        sort_options = search.SortOptions(
            expressions=expr
        )
        #build query options
        query_options = search.QueryOptions(
            limit = 20,
            sort_options=sort_options,
            snippeted_fields=["description"]
        )
        #build query object
        query_obj = search.Query(
            query_string=search_term,
            options=query_options
        )

        #perform search with query object
        results = search.Index('group').search(query=query_obj)

        groups = results.results

        image = '/img/photos/endofyearstellies.jpg'
        if groups:
            index = randint(0, len(groups)-1)
            imageFields = filter(lambda x: x.name == 'image', groups[index].fields)
            image = imageFields[0].value

        template_parms = {
            'groups': groups,
            'term': search_term,
            'background_image': image           
        }

        self.render('search.html',template_parms)
