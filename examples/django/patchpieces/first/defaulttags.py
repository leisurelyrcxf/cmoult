#django.template.defaulttags


import sys

defaulttags = sys.modules['django.template.defaulttags']

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



from pymoult.highlevel.updates import *

uUpdate = SafeRedefineUpdate(defaulttags,defaulttags.firstof,firstof)


