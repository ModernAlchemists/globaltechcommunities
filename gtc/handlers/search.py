#Google Apis
from google.appengine.api import search

# Custom importing
from gtc.handlers.base import BaseHandler
import gtc.schema as schema

class SearchHandler(BaseHandler):

  def get(self):
    search_term = self.request.get('search-term')
    if not search_term:
        self.redirect('/')
    else:
        index = search.Index('group')
        snippet = "snippet(%s,description,140)" % search_term

        options = search.QueryOptions(
            returned_expressions=[
                search.FieldExpression(name='snippet', expression=snippet)
            ]
        )

        result = index.search(
            query=search.Query(
                query_string=search_term,
                options=options
            )
        )

        groups = []
        if result:
            groups = result.results

        template_parms = {
            'groups': groups,
            'term': search_term
        }

        self.render('search.html',template_parms)
    