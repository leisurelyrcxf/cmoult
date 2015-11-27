#django.db.models.query_utils
import sys

utils = sys.modules['django.db.models.query_utils']

#class Q
def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
      # We must promote any new joins to left outer joins so that when Q is
      # used as an expression, rows aren't filtered due to joins.
      joins_before = query.tables[:]
      clause, joins = query._add_q(self, reuse, allow_joins=allow_joins, split_subq=False)
      joins_to_promote = [j for j in joins if j not in joins_before]
      query.promote_joins(joins_to_promote)
      return clause


from pymoult.highlevel.updates import *

cUpdate = SafeRedefineMethodUpdate(utils.Q,utils.Q.resolve_expression,resolve_expression)



    


