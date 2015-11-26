#django.contrib.admindocs.utils
import docutils.core
from django.utils.safestring import mark_safe

import sys

utils = sys.modules['django.contrib.admindocs.utils']


def parse_rst(text, default_reference_context, thing_being_parsed=None):
    """
    Convert the string from reST to an XHTML fragment.
    """
    overrides = {
        'doctitle_xform': True,
        'inital_header_level': 3,
        "default_reference_context": default_reference_context,
        "link_base": reverse('django-admindocs-docroot').rstrip('/'),
        'raw_enabled': False,
        'file_insertion_enabled': False
    }
    if thing_being_parsed:
        thing_being_parsed = force_bytes("<%s>" % thing_being_parsed)
    # Wrap ``text`` in some reST that sets the default role to ``cmsreference``,
    # then restores it.
    source = """
.. default-role:: cmsreference

%s

.. default-role::
"""
    parts = docutils.core.publish_parts(source % text,
                source_path=thing_being_parsed, destination_path=None,
                writer_name='html', settings_overrides=overrides)
    return mark_safe(parts['fragment'])


from pymoult.highlevel.updates import *

uUpdate = SafeRedefineUpdate(utils,utils.parse_rst,parse_rst,"parse_rst")


