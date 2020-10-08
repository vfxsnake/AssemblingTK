import sys

sys.path.append('D:/zebratv/Projects/BOLO/software/AssemblingTK/src/LightingTK/') if 'D:/zebratv/Projects/BOLO/software/AssemblingTK/src/LightingTK/' not in sys.path else None

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


if __name__ == '__main__':
    import window

    #app= QApplication(sys.argv)
    window = window.ImageDialog()
    window.Show()
    #sys.exit(app.exec_())

