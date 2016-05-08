# coding=utf-8

import time
import logging

from PySide import QtGui, QtCore
from getdata import Get_data
from gs_interface import YS232

class Data_Thread(QtCore.QThread):
    def __init__(self, time_delay, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.time_delay = time_delay

    def run(self):
        while self.exiting is False:
            sun_location = Get_data()
            sun_location_data = sun_location.get_data()

            self.emit(QtCore.SIGNAL("progress(float, float, float)"), sun_location_data[0],
                      sun_location_data[1], sun_location_data[2])
            time.sleep(self.time_delay)

    def stop(self):
        self.exiting = True


class Serial_Thread(QtCore.QThread):
    def __init__(self, time_delay, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.minimum_time_delay = time_delay

        self.serial_connection = YS232('Test_connection', 500000, 8, 'YES', 1,
                                       '/dev/ttyUSB0')

    def run(self):
        while self.exiting is False:
            answer = self.serial_connection.send_position(1, 2)
            self.emit(QtCore.SIGNAL("serial(int)"), answer)
            time.sleep(self.minimum_time_delay)

    def stop(self):
        logging.debug('Stopped')
        self.exiting = True


class WriteStream(object):
    """
    Messages from standard output are save to a queue object.

    """
    def __init__(self, queue):
        """ Init method.

        @param queue: The queue created for register the text messages.
        @return: None.
        """
        self.queue = queue

    def write(self, text):
        """ Write method.
        Append a new element to the queue.

        @param text: Text string to be show in screen.
        @return: None
        """
        self.queue.put(text)

    # TODO Improve description
    def flush(self):
        """

        @return:
        """
        pass


class MessagesThread(QtCore.QThread):
    """
    A QObject (to be run in a QThread) which sits waiting for data to come
    through a Queue.Queue().
    It blocks until data is available, and one it has got something from the
    queue, it sends it to the "MainThread" by emitting a Qt Signal
    """
    mysignal = QtCore.Signal(str)

    def __init__(self, queue, *args, **kwargs):
        """

        @param queue: queue object already created.
        @param args: Inhered, Not used
        @param kwargs: Inhered. Not used.
        @return: None.
        """
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.queue = queue

    @QtCore.Slot()
    def run(self):
        """

        @return:
        """
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)