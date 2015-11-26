#django.db.models.sql.compiler

import sys

compiler = sys.modules['django.db.models.sql.compiler']

#class SQLCompiler

def get_order_by(self):
    """
    Returns a list of 2-tuples of form (expr, (sql, params)) for the
    ORDER BY clause.
    
    The order_by clause can alter the select clause (for example it
    can add aliases to clauses that do not yet have one, or it can
    add totally new select clauses).
    """
    if self.query.extra_order_by:
        ordering = self.query.extra_order_by
    elif not self.query.default_ordering:
        ordering = self.query.order_by
    else:
        ordering = (self.query.order_by or self.query.get_meta().ordering or [])
    if self.query.standard_ordering:
        asc, desc = ORDER_DIR['ASC']
    else:
        asc, desc = ORDER_DIR['DESC']

    order_by = []
    for pos, field in enumerate(ordering):
        if hasattr(field, 'resolve_expression'):
            if not isinstance(field, OrderBy):
                field = field.asc()
            if not self.query.standard_ordering:
                field.reverse_ordering()
            order_by.append((field, False))
            continue
        if field == '?':  # random
            order_by.append((OrderBy(Random()), False))
            continue

        col, order = get_order_dir(field, asc)
        descending = True if order == 'DESC' else False

        if col in self.query.annotation_select:
            # Reference to expression in SELECT clause
            order_by.append((
                OrderBy(Ref(col, self.query.annotation_select[col]), descending=descending),
                True))
            continue
        if col in self.query.annotations:
            # References to an expression which is masked out of the SELECT clause
            order_by.append((
                OrderBy(self.query.annotations[col], descending=descending),
                False))
            continue

        if '.' in field:
            # This came in through an extra(order_by=...) addition. Pass it
            # on verbatim.
            table, col = col.split('.', 1)
            order_by.append((
                OrderBy(
                    RawSQL('%s.%s' % (self.quote_name_unless_alias(table), col), []),
                    descending=descending
                ), False))
            continue

        if not self.query._extra or col not in self.query._extra:
            # 'col' is of the form 'field' or 'field1__field2' or
            # '-field1__field2__field', etc.
            order_by.extend(self.find_ordering_name(
                field, self.query.get_meta(), default_order=asc))
        else:
            if col not in self.query.extra_select:
                order_by.append((
                    OrderBy(RawSQL(*self.query.extra[col]), descending=descending),
                    False))
            else:
                order_by.append((
                    OrderBy(Ref(col, RawSQL(*self.query.extra[col])), descending=descending),
                    True))
    result = []
    seen = set()
    
    for expr, is_ref in order_by:
        resolved = expr.resolve_expression(
            self.query, allow_joins=True, reuse=None)
        sql, params = self.compile(resolved)
        # Don't add the same column twice, but the order direction is
        # not taken into account so we strip it. When this entire method
        # is refactored into expressions, then we can check each part as we
        # generate it.
        without_ordering = self.ordering_parts.search(sql).group(1)
        if (without_ordering, tuple(params)) in seen:
            continue
        seen.add((without_ordering, tuple(params)))
        result.append((resolved, (sql, params, is_ref)))
    return result


def quote_name_unless_alias(self, name):
    """
    A wrapper around connection.ops.quote_name that doesn't quote aliases
    for table names. This avoids problems with some SQL dialects that treat
    quoted strings specially (e.g. PostgreSQL).
    """
    if name in self.quote_cache:
        return self.quote_cache[name]
    if ((name in self.query.alias_map and name not in self.query.table_map) or
        name in self.query.extra_select or (
            name in self.query.external_aliases and name not in self.query.table_map)):
        self.quote_cache[name] = name
        return name
    r = self.connection.ops.quote_name(name)
    self.quote_cache[name] = r
    return r


#class SQLUpdateCompiler
def as_sql(self):
    """
    Creates the SQL for this query. Returns the SQL string and list of
    parameters.
    """
    self.pre_sql_setup()
    if not self.query.values:
        return '', ()
    table = self.query.tables[0]
    qn = self.quote_name_unless_alias
    result = ['UPDATE %s' % qn(table)]
    result.append('SET')
    values, update_params = [], []
    for field, model, val in self.query.values:
        if hasattr(val, 'resolve_expression'):
            val = val.resolve_expression(self.query, allow_joins=False, for_save=True)
            if val.contains_aggregate:
                raise FieldError("Aggregate functions are not allowed in this query")
        elif hasattr(val, 'prepare_database_save'):
            if field.rel:
                val = field.get_db_prep_save(
                    val.prepare_database_save(field),
                    connection=self.connection,
                )
            else:
                raise TypeError("Database is trying to update a relational field "
                                "of type %s with a value of type %s. Make sure "
                                "you are setting the correct relations" %
                                (field.__class__.__name__, val.__class__.__name__))
        else:
            val = field.get_db_prep_save(val, connection=self.connection)
            
        # Getting the placeholder for the field.
        if hasattr(field, 'get_placeholder'):
            placeholder = field.get_placeholder(val, self, self.connection)
        else:
            placeholder = '%s'
        name = field.column
        if hasattr(val, 'as_sql'):
            sql, params = self.compile(val)
            values.append('%s = %s' % (qn(name), sql))
            update_params.extend(params)
        elif val is not None:
            values.append('%s = %s' % (qn(name), placeholder))
            update_params.append(val)
        else:
            values.append('%s = NULL' % qn(name))
    if not values:
        return '', ()
    result.append(', '.join(values))
    where, params = self.compile(self.query.where)
    if where:
        result.append('WHERE %s' % where)
    return ' '.join(result), tuple(update_params + params)



from pymoult.highlevel.updates import *

comp1Update = SafeRedefineMethodUpdate(compiler.SQLCompiler,compiler.SQLCompiler.get_order_by,get_order_by)

comp2Update = SafeRedefineMethodUpdate(compiler.SQLCompiler,compiler.SQLCompiler.quote_name_unless_alias,quote_name_unless_alias)


comp3Update= SafeRedefineMethodUpdate(compiler.SQLUpdateCompiler,compiler.SQLUpdateCompiler.as_sql,as_sql)
                                    


