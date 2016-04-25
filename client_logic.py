# coding=utf-8

# Create thread for UI
# Create thread for getting data

import sys
from PySide import QtGui

from client_ui import Main_window



app = QtGui.QApplication(sys.argv)
qapp = Main_window()
qapp.show()

sys.exit(app.exec_())
