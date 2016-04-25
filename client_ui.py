# coding=utf-8
from PySide import QtGui

from getdata import Get_data



class Main_window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icarus 0.1')

        self.user_data()

    def user_data(self):
        create = Get_data()

        blabla = create.get_data()
        print (blabla)
        print (type(blabla[0]))

        haha = str(blabla[0])


        label = QtGui.QLabel(self)
        label.setText(haha)
        label.show()
