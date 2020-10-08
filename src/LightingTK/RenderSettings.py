import pymel.core as pm

from PySide2 import QtUiTools

try:
    from PySide import QtCore
    from PySide import QtGui
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

import pymel.core as pm


def RedshiftRender():
    import pymel.core as pm
    pm.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")
    pm.inViewMessage(amg='<hl>!!!! Redshift Render !!!!</hl>.', pos='midCenter', fade=True)