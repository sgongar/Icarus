# coding=utf-8

from sys import argv, exit
import sys
import logging
from Queue import Queue
from time import gmtime

from PySide import QtGui

from threads import WriteStream, MessagesThread

textqueue = Queue()
sys.stdout = WriteStream(textqueue)

log_settings = logging.getLogger()
log_settings.setLevel(logging.DEBUG)

debug_log = logging.StreamHandler(sys.stdout)
debug_log.setLevel(logging.DEBUG)
debug_formatter = logging.Formatter('%(asctime)s - %(message)s')

debug_formatter.converter = gmtime

debug_log.setFormatter(debug_formatter)

log_settings.addHandler(debug_log)

logging.info('----- Icarus client ----')

app = QtGui.QApplication(argv)

from client_ui import Main_window
qapp = Main_window()
qapp.show()

messages_receiver = MessagesThread(textqueue)
messages_receiver.mysignal.connect(qapp.append_text)
messages_receiver.start()

exit(app.exec_())
