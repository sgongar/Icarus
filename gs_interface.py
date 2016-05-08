# coding=utf-8

import serial
import logging


class YS232():

    def __init__(self, name, baudrate, bytelength, parity, stopbits, port):
        self.name = name
        self.baudrate = baudrate
        # Longitud del byte.
        self.bytelength = bytelength
        # Paridad -- Esta variable es un string que puede valer "Si" o "No".
        self.parity = parity
        # Bits de parada -- Esta variable es un entero que puede valer 0 o 1.
        self.stopbits = int(stopbits)
        # Convertimos la variable port a una variable de tipo string.
        port = str(port)
        # La asignamos a la variable puerto.
        self.puerto = port

    def send_position(self, acimut, altura):
        try:
            send_serial = serial.Serial(self.puerto, self.baudrate, timeout=self.stopbits)

            send_serial.write("W%s %s" % (acimut, altura))

            send_serial.write("\r")
            send_serial.close()

            return 1
        except:
            logging.debug("Position not sended")

            return 0

    def parar_sistema(self):
        try:
            parar_serial = serial.Serial(self.puerto, self.baudrate, timeout=self.stopbits)
            parar_serial.write("S")
            parar_serial.write("\r")
            parar_serial.close()
        except:
            logging.debug('System not halted')

    def comprobar_conexion(self):
        try:
            comprobar_conexion = serial.Serial(self.puerto, self.baudrate)
            comprobar_conexion.timeout = None

            comprobar_conexion.write("C")
            comprobar_conexion.write("\n")

            # En este punto el controlador debería devolvernos una cadena de
            # caracteres del tipo +0aaa".

            # Mostramos un aviso por pantalla. Nos implementamos la recolecció
            # de los datos de vuelta porque no disponemos del rotor.
            print "Nos devuelve el acimut actual."

            # Envíamos el caracter B para que el sistema nos devuelva la altura.
            # comprobar_conexion.write("B")

            # En este punto el controlador debería devolvernos una cadena de
            #  caracteres del tipo +0aaa".
            # Volveremos a mostrar un aviso por pantalla llegados a este punto.
            print "Nos devuelve la elevacion actual."

            # Enviamos una señal para que nos devuelva datos (line feed).
            comprobar_conexion.write("\n")
            comprobar_conexion.close()
        except:
            logging.debug('Connection error')