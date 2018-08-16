#Google Apis
from google.appengine.api import search

# Custom importing
from gtc.handlers.base import BaseHandler
import gtc.schema as schema

class SearchHandler(BaseHandler):

  def get(self):
    search_terms = self.request.get('search-term').split(' ')

    if not search_terms:
        self.redirect('/')
    else:
        index = search.Index('group')
        expressions = []

        for term in search_terms:
            snippet = "snippet(%s,description,140)" % term
            expressions.append(search.FieldExpression(name='snippet', expression=snippet))

        options = search.QueryOptions(
            returned_expressions=expressions
        )

        result = index.search(
            query=search.Query(
                query_string=' '.join(search_terms),
                options=options
            )
        )

        groups = []
        if result:
            groups = result.results

        template_parms = {
            'groups': groups,
            'term': ' '.join(search_terms)
        }

        self.render('search.html',template_parms)
    