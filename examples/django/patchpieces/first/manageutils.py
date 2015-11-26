#django.core.management.utils

import sys

utils = sys.modules['django.core.management.utils']

def popen_wrapper(args, os_err_exc_type=CommandError, universal_newlines=True):
    """
    Friendly wrapper around Popen.

    Returns stdout output, stderr output and OS status code.
    """
    try:
        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE,
                close_fds=os.name != 'nt', universal_newlines=universal_newlines)
    except OSError as e:
        strerror = force_text(e.strerror, DEFAULT_LOCALE_ENCODING,
                              strings_only=True)
        six.reraise(os_err_exc_type, os_err_exc_type('Error executing %s: %s' %
                    (args[0], strerror)), sys.exc_info()[2])
    output, errors = p.communicate()
    return (
        output,
        force_text(errors, DEFAULT_LOCALE_ENCODING, strings_only=True),
        p.returncode
    )


from pymoult.highlevel.updates import *

u2Update = SafeRedefineUpdate(utils,utils.popen_wrapper,popen_wrapper,"popen_wrapper")


