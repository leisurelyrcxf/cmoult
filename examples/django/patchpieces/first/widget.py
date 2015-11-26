#django.contrib.admin.widget
from django.forms.widgets import Media
from django.contrib.admin.templatetags.admin_static import static
import sys

widget = sys.modules['django.contrib.admin.widget']

#class RelatedFieldWidgetWrapper
@property 
def media(self):
    media = Media(js=[static('admin/js/related-widget-wrapper.js')])
    return self.widget.media + media


from pymoult.highlevel.updates import *

wUpdate = SafeRedefineMethodUpdate(widget.RelatedFieldWidgetWrapper,widget.RelatedFieldWidgetWrapper.media,media,"media")


