#parsed




#django.db.models.sql.query
#from collections import Iterator, Mapping, OrderedDict

#class Query

 def build_filter(self, filter_expr, branch_negated=False, current_negated=False,
                     can_reuse=None, connector=AND, allow_joins=True):
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
        allow_many = not branch_negated

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


#django.template.defaulttags
#"register": from the module
@register.tag
def firstof(parser, token):
    """
    Outputs the first variable passed that is not False, without escaping.

    Outputs nothing if all the passed variables are False.

    Sample usage::

        {% firstof var1 var2 var3 %}

    This is equivalent to::

        {% if var1 %}
            {{ var1|safe }}
        {% elif var2 %}
            {{ var2|safe }}
        {% elif var3 %}
            {{ var3|safe }}
        {% endif %}

    but obviously much cleaner!

    You can also use a literal string as a fallback value in case all
    passed variables are False::

        {% firstof var1 var2 var3 "fallback value" %}

    If you want to disable auto-escaping of variables you can use::

        {% autoescape off %}
            {% firstof var1 var2 var3 "<strong>fallback value</strong>" %}
        {% autoescape %}

    Or if only some variables should be escaped, you can use::

        {% firstof var1 var2|safe var3 "<strong>fallback value</strong>"|safe %}

    """
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise TemplateSyntaxError("'firstof' statement requires at least one argument")
    return FirstOfNode([parser.compile_filter(bit) for bit in bits])

#django.utils.translation.trans_real
def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    lang = get_language()
    if lang is None:
        return False
    else:
        base_lang = get_language().split('-')[0]
        return base_lang in settings.LANGUAGES_BIDI

#lru_cache from django.utils
@lru_cache.lru_cache(maxsize=1000)
def check_for_language(lang_code):
    """
    Checks whether there is a global language file for the given language
    code. This is used to decide whether a user-provided language is
    available.

    lru_cache should have a maxsize to prevent from memory exhaustion attacks,
    as the provided language codes are taken from the HTTP request. See also
    <https://www.djangoproject.com/weblog/2007/oct/26/security-fix/>.
    """
    # First, a quick check to make sure lang_code is well-formed (#21458)
    if lang_code is None or not language_code_re.search(lang_code):
        return False
    for path in all_locale_paths():
        if gettext_module.find('django', path, [to_locale(lang_code)]) is not None:
            return True
    return False


















#Updates script
from pymoult.highlevel.updates import *
from pymoult.highlevel.managers import *
import sys




manager = ThreadedManager(name="PymoultManager")
manager.start()


#django.contrib.admin.widget
from patchpieces.first.widget import wUpdate
manager.add_update(wUpdate)

#django.contrib.admindocs.utils
from patchpieces.first.admdocutils import uUpdate
manager.add_update(uUpdate)
