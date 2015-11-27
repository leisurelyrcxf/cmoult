#parsed

import sys
#New code in patchpieces/first







#Updates script
from pymoult.highlevel.updates import *
from pymoult.highlevel.managers import *





manager = ThreadedManager(name="PymoultManager")
manager.start()


#django.contrib.admin.widget
from patchpieces.first.widget import wUpdate
manager.add_update(wUpdate)

#django.contrib.admindocs.utils
from patchpieces.first.admdocutils import uUpdate
manager.add_update(uUpdate)
