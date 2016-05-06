# coding=utf-8
from PySide import QtGui, QtCore

from getdata import Get_data
from threads import MyThread


class Main_window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(400, 400, 800, 400)
        self.setWindowTitle('Icarus 0.1')

        self.thread = MyThread()
        self.connect(self.thread, QtCore.SIGNAL("progress(float, float)"), self.progress)

        self.altitude = QtGui.QLabel(self)
        self.azimuth = QtGui.QLabel(self)
        self.create_ui()

        self.thread.start()

    def progress(self, alt, az):
        self.print_data(alt, az)

    def create_ui(self):
        """

        :return:
        """
        text_bullseye = QtGui.QLabel(self)
        text_bullseye.setText("Sun location")
        text_bullseye.move(450, 20)

        bullseye = QtGui.QPixmap("images/bullseye.png")
        label_bullseye = QtGui.QLabel(self)
        label_bullseye.setPixmap(bullseye)
        label_bullseye.move(450, 50)

        label_observer = QtGui.QLabel(self)
        label_observer.setText('Observer')
        label_observer.move(200, 200) # 20, 20
        label_altitude = QtGui.QLabel(self)
        label_altitude.setText('Altitude')
        label_altitude.move(20, 40)
        label_azimuth = QtGui.QLabel(self)
        label_azimuth.setText('Azimuth ')
        label_azimuth.move(20, 60)

        text_bullseye.show()
        label_bullseye.show()
        label_observer.show()
        label_altitude.show()
        label_azimuth.show()

        self.altitude.setText('')
        self.azimuth.setText('')

        self.altitude.move(20, 20) # was 100,40
        self.azimuth.move(100, 60)

        self.altitude.show()
        self.azimuth.show()

    def print_data(self, alt, az):
        """

        :param alt:
        :param az:
        :return:
        """
        print (type(alt))
        self.altitude.setFloat(alt)
        # self.azimuth.setText(az)


