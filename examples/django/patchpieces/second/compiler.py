#django.db.models.sql.query
import sys

query = sys.modules['django.db.models.sql.query']
#class Query
def build_filter(self, filter_expr, branch_negated=False, current_negated=False,
                    can_reuse=None, connector=AND, allow_joins=True, split_subq=True):
       """
       Builds a WhereNode for a single filter clause, but doesn't add it
       to this Query. Query.add_q() will then add this filter to the where
       or having Node.

       The 'branch_negated' tells us if the current branch contains any
       negations. This will be used to determine if subqueries are needed.

       The 'current_negated' is used to determine if the current filter is
       negated or not and this will be used to determine if IS NULL filtering
       is needed.

       The difference between current_netageted and branch_negated is that
       branch_negated is set on first negation, but current_negated is
       flipped for each negation.

       Note that add_filter will not do any negating itself, that is done
       upper in the code by add_q().

       The 'can_reuse' is a set of reusable joins for multijoins.

       The method will create a filter clause that can be added to the current
       query. However, if the filter isn't added to the query then the caller
       is responsible for unreffing the joins used.
       """
       arg, value = filter_expr
       if not arg:
           raise FieldError("Cannot parse keyword query %r" % arg)
       lookups, parts, reffed_aggregate = self.solve_lookup_type(arg)
       if not allow_joins and len(parts) > 1:
           raise FieldError("Joined field references are not permitted in this query")

       # Work out the lookup type and remove it from the end of 'parts',
       # if necessary.
       value, lookups, used_joins = self.prepare_lookup_value(value, lookups, can_reuse, allow_joins)

       clause = self.where_class()
       if reffed_aggregate:
           condition = self.build_lookup(lookups, reffed_aggregate, value)
           if not condition:
               # Backwards compat for custom lookups
               assert len(lookups) == 1
               condition = (reffed_aggregate, lookups[0], value)
           clause.add(condition, AND)
           return clause, []

       opts = self.get_meta()
       alias = self.get_initial_alias()
       allow_many = not branch_negated or not split_subq

       try:
           field, sources, opts, join_list, path = self.setup_joins(
               parts, opts, alias, can_reuse=can_reuse, allow_many=allow_many)

           # Prevent iterator from being consumed by check_related_objects()
           if isinstance(value, Iterator):
               value = list(value)
           self.check_related_objects(field, value, opts)

           # split_exclude() needs to know which joins were generated for the
           # lookup parts
           self._lookup_joins = join_list
       except MultiJoin as e:
           return self.split_exclude(filter_expr, LOOKUP_SEP.join(parts[:e.level]),
                                     can_reuse, e.names_with_path)

       if can_reuse is not None:
           can_reuse.update(join_list)
       used_joins = set(used_joins).union(set(join_list))

       # Process the join list to see if we can remove any non-needed joins from
       # the far end (fewer tables in a query is better).
       targets, alias, join_list = self.trim_joins(sources, join_list, path)

       if hasattr(field, 'get_lookup_constraint'):
           # For now foreign keys get special treatment. This should be
           # refactored when composite fields lands.
           condition = field.get_lookup_constraint(self.where_class, alias, targets, sources,
                                                   lookups, value)
           lookup_type = lookups[-1]
       else:
           assert(len(targets) == 1)
           if hasattr(targets[0], 'as_sql'):
               # handle Expressions as annotations
               col = targets[0]
           else:
               col = targets[0].get_col(alias, field)
           condition = self.build_lookup(lookups, col, value)
           if not condition:
               # Backwards compat for custom lookups
               if lookups[0] not in self.query_terms:
                   raise FieldError(
                       "Join on field '%s' not permitted. Did you "
                       "misspell '%s' for the lookup type?" %
                       (col.output_field.name, lookups[0]))
               if len(lookups) > 1:
                   raise FieldError("Nested lookup '%s' not supported." %
                                    LOOKUP_SEP.join(lookups))
               condition = (Constraint(alias, targets[0].column, field), lookups[0], value)
               lookup_type = lookups[-1]
           else:
               lookup_type = condition.lookup_name

       clause.add(condition, AND)

       require_outer = lookup_type == 'isnull' and value is True and not current_negated
       if current_negated and (lookup_type != 'isnull' or value is False):
           require_outer = True
           if (lookup_type != 'isnull' and (
                   self.is_nullable(targets[0]) or
                   self.alias_map[join_list[-1]].join_type == LOUTER)):
               # The condition added here will be SQL like this:
               # NOT (col IS NOT NULL), where the first NOT is added in
               # upper layers of code. The reason for addition is that if col
               # is null, then col != someval will result in SQL "unknown"
               # which isn't the same as in Python. The Python None handling
               # is wanted, and it can be gotten by
               # (col IS NULL OR col != someval)
               #   <=>
               # NOT (col IS NOT NULL AND col = someval).
               lookup_class = targets[0].get_lookup('isnull')
               clause.add(lookup_class(targets[0].get_col(alias, sources[0]), False), AND)
       return clause, used_joins if not require_outer else ()

def _add_q(self, q_object, used_aliases, branch_negated=False,
           current_negated=False, allow_joins=True, split_subq=True):
      """
      Adds a Q-object to the current filter.
      """
      connector = q_object.connector
      current_negated = current_negated ^ q_object.negated
      branch_negated = branch_negated or q_object.negated
      target_clause = self.where_class(connector=connector,
                                       negated=q_object.negated)
      joinpromoter = JoinPromoter(q_object.connector, len(q_object.children), current_negated)
      for child in q_object.children:
            if isinstance(child, Node):
                  child_clause, needed_inner = self._add_q(
                        child, used_aliases, branch_negated,
                        current_negated, allow_joins, split_subq)
                  joinpromoter.add_votes(needed_inner)
            else:
                  child_clause, needed_inner = self.build_filter(
                        child, can_reuse=used_aliases, branch_negated=branch_negated,
                        current_negated=current_negated, connector=connector,
                        allow_joins=allow_joins, split_subq=split_subq,
                  )
                  joinpromoter.add_votes(needed_inner)
            target_clause.add(child_clause, connector)
      needed_inner = joinpromoter.update_join_types(self)
      return target_clause, needed_inner

from pymoult.highlevel.updates import *

q1Update = SafeRedefineMethodUpdate(query.Query,query.Query.build_filter,build_filter)
q1Update = SafeRedefineMethodUpdate(query.Query,query.Query._add_q,_add_q)



    


