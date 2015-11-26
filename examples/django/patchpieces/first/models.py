#django.db.migrations.operations.models
import sys

models = sys.modules['django.db.migrations.operations.models']

#class RenameModel
def state_forwards(self, app_label, state):
    apps = state.apps
    model = apps.get_model(app_label, self.old_name)
    model._meta.apps = apps
    # Get all of the related objects we need to repoint
    all_related_objects = (
        f for f in model._meta.get_fields(include_hidden=True)
        if f.auto_created and not f.concrete and (not f.hidden or f.many_to_many)
    )
    # Rename the model
    state.models[app_label, self.new_name_lower] = state.models[app_label, self.old_name_lower]
    state.models[app_label, self.new_name_lower].name = self.new_name
    state.remove_model(app_label, self.old_name_lower)
    # Repoint the FKs and M2Ms pointing to us
    for related_object in all_related_objects:
        if related_object.model is not model:
            # The model being renamed does not participate in this relation
            # directly. Rather, a superclass does.
            continue
        # Use the new related key for self referential related objects.
        if related_object.related_model == model:
            related_key = (app_label, self.new_name_lower)
        else:
            related_key = (
                related_object.related_model._meta.app_label,
                related_object.related_model._meta.model_name,
            )
        new_fields = []
        for name, field in state.models[related_key].fields:
            if name == related_object.field.name:
                field = field.clone()
                field.rel.to = "%s.%s" % (app_label, self.new_name)
            new_fields.append((name, field))
        state.models[related_key].fields = new_fields
        state.reload_model(*related_key)
    state.reload_model(app_label, self.new_name_lower)


from pymoult.highlevel.updates import *

mUpdate = SafeRedefineMethodUpdate(models.RenameModel,models.RenameModel.state_forwards,state_forwards,"state_forwards")


