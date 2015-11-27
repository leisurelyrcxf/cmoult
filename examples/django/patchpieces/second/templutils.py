#django.template.utils
import sys

utils = sys.modules['django.template.utils']

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

from pymoult.highlevel.updates import *

uUpdate = SafeRedefineMethodUpdate(utils.EngineHandler,utils.EngineHandler.templates,templates)



    


