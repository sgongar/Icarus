# coding=utf-8
import logging

from PySide import QtGui, QtCore

from threads import Data_Thread, Serial_Thread
from misc import convert_data_to_draw, get_serial_ports


class Main_window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(400, 400, 800, 400)
        self.setWindowTitle('Icarus 0.1')

        self.create_ui()
        self.initConsole()

        # TODO time_delay hard-coded
        self.get_data_thread = Data_Thread(time_delay=4)
        self.connect(self.get_data_thread, QtCore.SIGNAL("progress(float, float, float)"),
                     self.progress)
        self.get_data_thread.start()

        # TODO time_delay hard-coded
        self.serial_connection_thread = Serial_Thread(time_delay=4)
        self.connect(self.serial_connection_thread, QtCore.SIGNAL("serial(int)"),
                     self.serial_data)

        self.setFont(QtGui.QFont('SansSerif', 11))

        self.x = 615
        self.y = 195

    def progress(self, alt, az, timestamp):
        """

        :param alt:
        :param az:
        :param timestamp:
        :return:
        """
        if alt < 0:
            logging.debug("Below horizon")
            self.get_data_thread.stop()
            self.serial_connection_thread.stop()
        else:
            self.print_data(alt, az, timestamp)
            self.draw_data(alt, az)

    def create_ui(self):
        """

        :return:
        """
        bullseye = QtGui.QPixmap("images/bullseye.png")
        label_bullseye = QtGui.QLabel(self)
        label_bullseye.setPixmap(bullseye)
        label_bullseye.move(470, 50)

        labels = QtGui.QGroupBox(self)
        labels_grid = QtGui.QGridLayout(labels)
        labels.setLayout(labels_grid)

        label_observer = QtGui.QLabel(self)
        label_observer.setText('Observer: ')
        label_observer.setFixedWidth(100)
        label_observer.setFixedHeight(25)
        label_altitude = QtGui.QLabel(self)
        label_altitude.setText('Altitude: ')
        label_altitude.setFixedWidth(100)
        label_altitude.setFixedHeight(25)
        label_azimuth = QtGui.QLabel(self)
        label_azimuth.setText('Azimuth:  ')
        label_azimuth.setFixedWidth(100)
        label_azimuth.setFixedHeight(25)
        label_connection = QtGui.QLabel(self)
        label_connection.setText('Connection:')
        label_connection.setFixedWidth(100)
        label_connection.setFixedHeight(25)

        self.observer = QtGui.QLabel(self)
        self.observer.setText('UPCT')
        self.observer.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.altitude = QtGui.QLabel(self)
        self.altitude.setText('')
        self.altitude.setFixedWidth(100)
        self.altitude.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.azimuth = QtGui.QLabel(self)
        self.azimuth.setText('')
        self.azimuth.setFixedWidth(100)
        self.azimuth.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.connection_status = QtGui.QLabel(self)
        self.connection_status.setText('Halted')
        self.connection_status.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.port_selection = QtGui.QComboBox(self)

        labels_grid.addWidget(label_observer, 0, 0, 1, 1)
        labels_grid.addWidget(self.observer, 0, 1, 1, 1)
        labels_grid.addWidget(label_altitude, 1, 0, 1, 1)
        labels_grid.addWidget(self.altitude, 1, 1, 1, 1)
        labels_grid.addWidget(label_azimuth, 2, 0, 1, 1)
        labels_grid.addWidget(self.azimuth, 2, 1, 1, 1)
        labels_grid.addWidget(label_connection, 3, 0, 1, 1)
        labels_grid.addWidget(self.connection_status, 3, 1, 1, 1)

        configuration = QtGui.QGroupBox(self)
        configuration_grid = QtGui.QGridLayout(configuration)
        configuration.setLayout(configuration_grid)

        load_button = QtGui.QPushButton("Load user")
        load_button.clicked.connect(self.load_user)
        configuration_button = QtGui.QPushButton("Set configuration")
        configuration_button.clicked.connect(self.configuration_window)

        configuration_grid.addWidget(load_button, 1, 0, 1, 1)
        configuration_grid.addWidget(configuration_button, 2, 0, 1, 1)

        configuration.move(260, 0)

        buttons = QtGui.QGroupBox(self)
        buttons_grid = QtGui.QGridLayout(buttons)
        buttons.setLayout(buttons_grid)

        label_port = QtGui.QLabel(self)
        label_port.setText('Port:')
        label_port.setFixedWidth(50)
        label_port.setFixedHeight(25)
        serial_ports = get_serial_ports()
        self.port_selection.addItems(serial_ports)
        self.port_selection.setFixedWidth(160)
        space = QtGui.QLabel(self)
        space.setFixedWidth(20)
        self.toggle_connection = QtGui.QPushButton("Connection")
        self.toggle_connection.setFixedWidth(150)
        self.toggle_connection.clicked.connect(self.connection)
        self.toggle_connection.setCheckable(True)

        buttons_grid.addWidget(label_port, 0, 1, 1, 1)
        buttons_grid.addWidget(self.port_selection, 0, 2, 1, 1)
        buttons_grid.addWidget(space, 0, 3, 1, 1)
        buttons_grid.addWidget(self.toggle_connection, 0, 4, 1, 1)
        buttons.move(5, 140)

    def load_user(self):
        logging.debug("Users window")

    def configuration_window(self):
        logging.debug("Configuration window")

    def connection(self):
        test = self.serial_connection_thread.start()

    def initConsole(self):
        self.console = QtGui.QTextBrowser(self)
        self.console.move(20, 210)
        self.console.resize(400, 180)
        self.console.setFont(QtGui.QFont('SansSerif', 11))

    def serial_data(self, i):
        if i == 0:
            self.serial_connection_thread.stop()
            self.toggle_connection.setText("Connection")
            self.connection_status.setText("Halted")
        elif i == 1:
            self.toggle_connection.setText("Disconnection")
            self.connection_status.setText("Established!")

    def print_data(self, alt, az, timestamp):
        """

        :param alt:
        :param az:
        :return:
        """
        from ephem import degrees
        self.altitude.setText(str(degrees(alt)))
        self.azimuth.setText(str(degrees(az)))

    def draw_data(self, alt, az):
        self.x, self.y = convert_data_to_draw(alt, az)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        brush = QtGui.QBrush(QtCore.Qt.darkBlue)
        qp.setBrush(brush)
        qp.drawRect(self.x, self.y, 10, 10)

    def append_text(self, text):
        self.console.append(text)