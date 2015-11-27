#django.utils.translation.trans_real

import sys

real = sys.modules['django.utils.translation.trans_real']

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




    
from pymoult.highlevel.updates import *

tt1Update = SafeRedefineUpdate(real,real.get_language_bidi,get_language_bidi)
tt2Update = SafeRedefineUpdate(real,real.check_for_language,check_for_language)

