#django.core.management.commands.makemessages

import sys

makemessages = sys.modules['django.core.management.commands.makemessages']

def gettext_popen_wrapper(args, os_err_exc_type=CommandError, stdout_encoding="utf-8"):
    """
    Makes sure text obtained from stdout of gettext utilities is Unicode.
    """
    # This both decodes utf-8 and cleans line endings. Simply using
    # popen_wrapper(universal_newlines=True) doesn't properly handle the
    # encoding. This goes back to popen's flaky support for encoding:
    # https://bugs.python.org/issue6135. This is a solution for #23271, #21928.
    # No need to do anything on Python 2 because it's already a byte-string there.
    manual_io_wrapper = six.PY3 and stdout_encoding != DEFAULT_LOCALE_ENCODING

    stdout, stderr, status_code = popen_wrapper(args, os_err_exc_type=os_err_exc_type,
                                                universal_newlines=not manual_io_wrapper)
    if manual_io_wrapper:
        stdout = io.TextIOWrapper(io.BytesIO(stdout), encoding=stdout_encoding).read()
    if six.PY2:
        stdout = stdout.decode(stdout_encoding)
    return stdout, stderr, status_code

from pymoult.highlevel.updates import *

mUpdate = SafeRedefineUpdate(makemessages,makemessages.gettext_popen_wrapper,gettext_popen_wrapper,"gettext_popen_wrapper")


