# coding=utf-8

# Create thread for UI
# Create thread for getting data

from sys import argv, exit

from PySide import QtGui

app = QtGui.QApplication(argv)
from client_ui import Main_window
qapp = Main_window()
qapp.show()

exit(app.exec_())
