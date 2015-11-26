#django.contrib.admin.widget
import sys

views = sys.modules['django.contrib.admindocs.views']
def get_context_data(self, **kwargs):
    model_name = self.kwargs['model_name']
    # Get the model class.
    try:
        app_config = apps.get_app_config(self.kwargs['app_label'])
    except LookupError:
        raise Http404(_("App %(app_label)r not found") % self.kwargs)
    try:
        model = app_config.get_model(model_name)
    except LookupError:
        raise Http404(_("Model %(model_name)r not found in app %(app_label)r") % self.kwargs)
    
    opts = model._meta

    title, body, metadata = utils.parse_docstring(model.__doc__)
    if title:
        title = utils.parse_rst(title, 'model', _('model:') + model_name)
    if body:
        body = utils.parse_rst(body, 'model', _('model:') + model_name)

    # Gather fields/field descriptions.
    fields = []
    for field in opts.fields:
        # ForeignKey is a special case since the field will actually be a
        # descriptor that returns the other object
        if isinstance(field, models.ForeignKey):
            data_type = field.rel.to.__name__
            app_label = field.rel.to._meta.app_label
            verbose = utils.parse_rst(
                (_("the related `%(app_label)s.%(data_type)s` object") % {
                    'app_label': app_label, 'data_type': data_type,
                }),
                'model',
                _('model:') + data_type,
            )
        else:
            data_type = get_readable_field_data_type(field)
            verbose = field.verbose_name
            fields.append({
            'name': field.name,
                'data_type': data_type,
                'verbose': verbose,
                'help_text': field.help_text,
            })

    # Gather many-to-many fields.
    for field in opts.many_to_many:
        data_type = field.rel.to.__name__
        app_label = field.rel.to._meta.app_label
        verbose = _("related `%(app_label)s.%(object_name)s` objects") % {
            'app_label': app_label,
            'object_name': data_type,
        }
        fields.append({
            'name': "%s.all" % field.name,
            "data_type": 'List',
            'verbose': utils.parse_rst(_("all %s") % verbose, 'model', _('model:') + opts.model_name),
        })
        fields.append({
            'name': "%s.count" % field.name,
            'data_type': 'Integer',
            'verbose': utils.parse_rst(_("number of %s") % verbose, 'model', _('model:') + opts.model_name),
        })

    # Gather model methods.
    for func_name, func in model.__dict__.items():
        if (inspect.isfunction(func) and len(inspect.getargspec(func)[0]) == 1):
            try:
                for exclude in MODEL_METHODS_EXCLUDE:
                    if func_name.startswith(exclude):
                        raise StopIteration
            except StopIteration:
                continue
            verbose = func.__doc__
            if verbose:
                verbose = utils.parse_rst(utils.trim_docstring(verbose), 'model', _('model:') + opts.model_name)
                fields.append({
                    'name': func_name,
                    'data_type': get_return_data_type(func_name),
                    'verbose': verbose,
                })

    # Gather related objects
    for rel in opts.related_objects:
        verbose = _("related `%(app_label)s.%(object_name)s` objects") % {
            'app_label': rel.related_model._meta.app_label, 
            'object_name': rel.related_model._meta.object_name,
        }
        accessor = rel.get_accessor_name()
        fields.append({
            'name': "%s.all" % accessor,
            'data_type': 'List',
            'verbose': utils.parse_rst(_("all %s") % verbose, 'model', _('model:') + opts.model_name),
        })
            fields.append({
                'name': "%s.count" % accessor,
                'data_type': 'Integer',
                'verbose': utils.parse_rst(_("number of %s") % verbose, 'model', _('model:') + opts.model_name),
            })
            kwargs.update({
                'name': '%s.%s' % (opts.app_label, opts.object_name),
                'summary': title,
                'description': body,
                'fields': fields,
            })
    return super(ModelDetailView, self).get_context_data(**kwargs)



from pymoult.highlevel.updates import *

vUpdate = SafeRedefineMethodUpdate(views.ModelDetailView,views.ModelDetailView.get_context_data,get_context_data,"get_context_data")


