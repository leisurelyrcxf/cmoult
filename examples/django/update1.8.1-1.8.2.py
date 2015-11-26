#parsed

#django.contrib.gis.admin.__init__
#from django.contrib.gis.admin.options import GeoModelAdmin, OSMGeoAdmin
#from django.contrib.gis.admin.widgets import OpenLayersWidget

__all__ = [
    'autodiscover', 'site', 'AdminSite', 'ModelAdmin', 'StackedInline',
    'TabularInline', 'HORIZONTAL', 'VERTICAL', 'GeoModelAdmin', 'OSMGeoAdmin',
    'OpenLayersWidget',
]

#django.contrib.gis.admin.options
#from django.core.exceptions import ImproperlyConfigured

spherical_mercator_srid = 3857

class OSMGeoAdmin(GeoModelAdmin):
    map_template = 'gis/admin/osm.html'
    num_zoom = 20
    map_srid = spherical_mercator_srid
    max_extent = '-20037508,-20037508,20037508,20037508'
    max_resolution = '156543.0339'
    point_zoom = num_zoom - 6
    units = 'm'

    def __init__(self, *args):
        if not HAS_GDAL:
            raise ImproperlyConfigured("OSMGeoAdmin is not usable without GDAL libs installed")
        super(OSMGeoAdmin, self).__init__(*args)

#django.contrib.prostgres.fields.hstore
class KeyTransform(Transform):
    output_field = TextField()

    def __init__(self, key_name, *args, **kwargs):
        super(KeyTransform, self).__init__(*args, **kwargs)
        self.key_name = key_name

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "(%s -> '%s')" % (lhs, self.key_name), params


#django.contrib.sessions.backends.cached_db
#class SessionStore
    def flush(self):
        """
        Removes the current session data from the database and regenerates the
        key.
        """
        self.clear()
        self.delete(self.session_key)
        self._session_key = None
#si session key est '' il doit valoir None

#django.contrib.sessions.middleware

class SessionMiddleware(object):
    def __init__(self):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            pass
        else:
            # First check if we need to delete this cookie.
            # The session should be deleted only if the session is entirely empty
            if settings.SESSION_COOKIE_NAME in request.COOKIES and empty:
                response.delete_cookie(settings.SESSION_COOKIE_NAME,
                    domain=settings.SESSION_COOKIE_DOMAIN)
            else:
                if accessed:
                    patch_vary_headers(response, ('Cookie',))
                if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                    if request.session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = cookie_date(expires_time)
                    # Save the session data and refresh the client cookie.
                    # Skip session save for 500 responses, refs #3881.
                    if response.status_code != 500:
                        request.session.save()
                        response.set_cookie(settings.SESSION_COOKIE_NAME,
                                request.session.session_key, max_age=max_age,
                                expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                path=settings.SESSION_COOKIE_PATH,
                                secure=settings.SESSION_COOKIE_SECURE or None,
                                httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response


#django.db.backends.base.creation
#class BaseDatabaseCreation

  def _destroy_test_db(self, test_database_name, verbosity):
        """
        Internal implementation - remove the test db tables.
        """
        # Remove the test database to clean up after
        # ourselves. Connect to the previous database (not the test database)
        # to do so, because it's not allowed to delete a database while being
        # connected to it.
        with self.connection._nodb_connection.cursor() as cursor:
            # Wait to avoid "database is being accessed by other users" errors.
            time.sleep(1)
            cursor.execute("DROP DATABASE %s"
                           % self.connection.ops.quote_name(test_database_name))

#django.db.backends.base.schema
#class BaseDatabaseSchemaEditor

    def alter_unique_together(self, model, old_unique_together, new_unique_together):
        """
        Deals with a model changing its unique_together.
        Note: The input unique_togethers must be doubly-nested, not the single-
        nested ["foo", "bar"] format.
        """
        olds = set(tuple(fields) for fields in old_unique_together)
        news = set(tuple(fields) for fields in new_unique_together)
        # Deleted uniques
        for fields in olds.difference(news):
            self._delete_composed_index(model, fields, {'unique': True}, self.sql_delete_unique)
        # Created uniques
        for fields in news.difference(olds):
            columns = [model._meta.get_field(field).column for field in fields]
            self.execute(self._create_unique_sql(model, columns))

    def alter_index_together(self, model, old_index_together, new_index_together):
        """
        Deals with a model changing its index_together.
        Note: The input index_togethers must be doubly-nested, not the single-
        nested ["foo", "bar"] format.
        """
        olds = set(tuple(fields) for fields in old_index_together)
        news = set(tuple(fields) for fields in new_index_together)
        # Deleted indexes
        for fields in olds.difference(news):
            self._delete_composed_index(model, fields, {'index': True}, self.sql_delete_index)
        # Created indexes
        for field_names in news.difference(olds):
            fields = [model._meta.get_field(field) for field in field_names]
            self.execute(self._create_index_sql(model, fields, suffix="_idx"))

    def _delete_composed_index(self, model, fields, constraint_kwargs, sql):
        columns = [model._meta.get_field(field).column for field in fields]
        constraint_names = self._constraint_names(model, columns, **constraint_kwargs)
        if len(constraint_names) != 1:
            raise ValueError("Found wrong number (%s) of constraints for %s(%s)" % (
                len(constraint_names),
                model._meta.db_table,
                ", ".join(columns),
            ))
        self.execute(self._delete_constraint_sql(sql, model, constraint_names[0]))

#django.db.backends.mysql.schema
#class DatabaseSchemaEditor
#Added
  def _delete_composed_index(self, model, fields, *args):
        """
        MySQL can remove an implicit FK index on a field when that field is
        covered by another index like a unique_together. "covered" here means
        that the more complex index starts like the simpler one.
        http://bugs.mysql.com/bug.php?id=37910 / Django ticket #24757
        We check here before removing the [unique|index]_together if we have to
        recreate a FK index.
        """
        first_field = model._meta.get_field(fields[0])
        if first_field.get_internal_type() == 'ForeignKey':
            constraint_names = self._constraint_names(model, fields[0], index=True)
            if not constraint_names:
                self.execute(
                    self._create_index_sql(model, [model._meta.get_field(fields[0])], suffix="")
                )
        return super(DatabaseSchemaEditor, self)._delete_composed_index(model, fields, *args)

#django.db.backends.postgresql_psycopg2.base
#import warnings
#from django.db import DEFAULT_DB_ALIAS
#from django.db.utils import DatabaseError as WrappedDatabaseError

#class DatabaseWrapper
   @cached_property
    def _nodb_connection(self):
        nodb_connection = super(DatabaseWrapper, self)._nodb_connection
        try:
            nodb_connection.ensure_connection()
        except (DatabaseError, WrappedDatabaseError):
            warnings.warn(
                "Normally Django will use a connection to the 'postgres' database "
                "to avoid running initialization queries against the production "
                "database when it's not needed (for example, when running tests). "
                "Django was unable to create a connection to the 'postgres' database "
                "and will use the default database instead.",
                RuntimeWarning
            )
            settings_dict = self.settings_dict.copy()
            settings_dict['NAME'] = settings.DATABASES[DEFAULT_DB_ALIAS]['NAME']
            nodb_connection = self.__class__(
                self.settings_dict.copy(),
                alias=self.alias,
                allow_thread_sharing=False)
        return nodb_connection

#django.db.backends.sqlite3.schema
#class DatabaseSchemaEditor
  def quote_value(self, value):
        # The backend "mostly works" without this function and there are use
        # cases for compiling Python without the sqlite3 libraries (e.g.
        # security hardening).
        import _sqlite3
        try:
            value = _sqlite3.adapt(value)
        except _sqlite3.ProgrammingError:
            pass
        # Manual emulation of SQLite parameter quoting
        if isinstance(value, type(True)):
            return str(int(value))
        elif isinstance(value, (Decimal, float)):
            return str(value)
        elif isinstance(value, six.integer_types):
            return str(value)
        elif isinstance(value, six.string_types):
            return "'%s'" % six.text_type(value).replace("\'", "\'\'")
        elif value is None:
            return "NULL"
        elif isinstance(value, (bytes, bytearray, six.memoryview)):
            # Bytes are only allowed for BLOB fields, encoded as string
            # literals containing hexadecimal data and preceded by a single "X"
            # character:
            # value = b'\x01\x02' => value_hex = b'0102' => return X'0102'
            value = bytes(value)
            hex_encoder = codecs.getencoder('hex_codec')
            value_hex, _length = hex_encoder(value)
            # Use 'ascii' encoding for b'01' => '01', no need to use force_text here.
            return "X'%s'" % value_hex.decode('ascii')
        else:
            raise ValueError("Cannot quote parameter value %r of type %s" % (value, type(value)))


#django.db.models.expressions
#class Case

    def copy(self):
        c = super(Case, self).copy()
        c.cases = c.cases[:]
        return c

#django.db.models.fields.related
#class ForeignKey

   def get_db_prep_value(self, value, connection, prepared=False):
        return self.related_field.get_db_prep_value(value, connection, prepared)

#django.db.models.query_utils
#class Q
    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        # We must promote any new joins to left outer joins so that when Q is
        # used as an expression, rows aren't filtered due to joins.
        joins_before = query.tables[:]
        clause, joins = query._add_q(self, reuse, allow_joins=allow_joins, split_subq=False)
        joins_to_promote = [j for j in joins if j not in joins_before]
        query.promote_joins(joins_to_promote)
        return clause

#django.db.models.sql.compiler
#class SQLCompiler

    def collapse_group_by(self, expressions, having):
        # If the DB can group by primary key, then group by the primary key of
        # query's main model. Note that for PostgreSQL the GROUP BY clause must
        # include the primary key of every table, but for MySQL it is enough to
        # have the main table's primary key. Currently only the MySQL form is
        # implemented.
        # MySQLism: however, columns in HAVING clause must be added to the
        # GROUP BY.
        if self.connection.features.allows_group_by_pk:
            # The logic here is: if the main model's primary key is in the
            # query, then set new_expressions to that field. If that happens,
            # then also add having expressions to group by.
            pk = None
            for expr in expressions:
                # Is this a reference to query's base table primary key? If the
                # expression isn't a Col-like, then skip the expression.
                if (getattr(expr, 'target', None) == self.query.model._meta.pk and
                        getattr(expr, 'alias', None) == self.query.tables[0]):
                    pk = expr
                    break
            if pk:
                expressions = [pk] + [expr for expr in expressions if expr in having]
        return expressions

#django.db.models.sql.query
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


#django.template.utils
#class EngineHandler

  @cached_property
    def templates(self):
        if self._templates is None:
            self._templates = settings.TEMPLATES

        if not self._templates:
            warnings.warn(
                "You haven't defined a TEMPLATES setting. You must do so "
                "before upgrading to Django 2.0. Otherwise Django will be "
                "unable to load templates.", RemovedInDjango20Warning)
            self._templates = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': settings.TEMPLATE_DIRS,
                    'OPTIONS': {
                        'allowed_include_roots': settings.ALLOWED_INCLUDE_ROOTS,
                        'context_processors': settings.TEMPLATE_CONTEXT_PROCESSORS,
                        'debug': settings.TEMPLATE_DEBUG,
                        'loaders': settings.TEMPLATE_LOADERS,
                        'string_if_invalid': settings.TEMPLATE_STRING_IF_INVALID,
                    },
                },
            ]

        templates = OrderedDict()
        backend_names = []
        for tpl in self._templates:
            tpl = tpl.copy()
            try:
                # This will raise an exception if 'BACKEND' doesn't exist or
                # isn't a string containing at least one dot.
                default_name = tpl['BACKEND'].rsplit('.', 2)[-2]
            except Exception:
                invalid_backend = tpl.get('BACKEND', '<not defined>')
                raise ImproperlyConfigured(
                    "Invalid BACKEND for a template engine: {}. Check "
                    "your TEMPLATES setting.".format(invalid_backend))

            tpl.setdefault('NAME', default_name)
            tpl.setdefault('DIRS', [])
            tpl.setdefault('APP_DIRS', False)
            tpl.setdefault('OPTIONS', {})

            templates[tpl['NAME']] = tpl
            backend_names.append(tpl['NAME'])

        counts = Counter(backend_names)
        duplicates = [alias for alias, count in counts.most_common() if count > 1]
        if duplicates:
            raise ImproperlyConfigured(
                "Template engine aliases aren't unique, duplicates: {}. "
                "Set a unique NAME for each engine in settings.TEMPLATES."
                .format(", ".join(duplicates)))

        return templates
