# coding=utf-8

import sys
import time

from PySide import QtGui, QtCore
from getdata import Get_data

class MyThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def run(self):
        while True:
            sun_location = Get_data()
            sun_location_data = sun_location.get_data()
            self.emit(QtCore.SIGNAL("progress(float, float)"), sun_location_data[0], sun_location_data[1])
            time.sleep(4)
