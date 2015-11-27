#django.db.models.expressions
import sys

expressions = sys.modules['django.db.models.expressions']

#class Case
def copy(self):
      c = super(Case, self).copy()
      c.cases = c.cases[:]
      return c


from pymoult.highlevel.updates import *

eUpdate = SafeRedefineMethodUpdate(expressions.Case,expressions.Case.copy,copy)



    


