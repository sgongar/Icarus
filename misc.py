# coding=utf-8
from os import path, getcwd
from ConfigParser import ConfigParser, SafeConfigParser

def get_data_from_file(settings_file):
    """

    :param settings_file: Settings file name.
    :return: A dictionary called location_info containing the data required.
    """
    if not path.isfile(settings_file):
        actual_dir = getcwd()
        settings_file_dir = actual_dir + '/' + settings_file
        print ("Settings file not present at %s", settings_file_dir)
        raise Exception

    location_info = {}
    config = ConfigParser()
    config.read(settings_file)

    location_info['lat'] = config.get('User', 'latitude')
    location_info['lon'] = config.get('User', 'longitude')

    return location_info


def set_data_local_file(settings_file, location_info):
    """

    :param settings_file: Settings file ame
    :param location_info: The new dictionary.
    :return:
    """
    old_location_info = get_data_from_file(settings_file)

    config = SafeConfigParser()
    config.read(settings_file)

    if location_info['lat'] is not old_location_info['lat']:
        config.set('User', 'latitude', str(location_info['lat']))
        with open(settings_file, 'wb') as configfile:
            config.write(configfile)

    if location_info['lon'] is not old_location_info['lon']:
        config.set('User', 'longitude', str(location_info['lon']))
        with open(settings_file, 'wb') as configfile:
            config.write(configfile)

    return True


def get_timestamp():
    """ TODO Implement time zones

    :return: A timestamp in ephem format
    """
    from time import time
    from datetime import datetime
    timestamp = time()

    st = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M')

    return st, timestamp


def convert_data_to_draw(alt, az):
    from math import degrees, pi
    from numpy import sin, cos
    rho = 150 - (150*degrees(alt))/90

    x = rho * sin(az)
    y = rho * cos(az)

    x = 595 + x
    y = 195 - y

    return(x, y)

def get_serial_ports():
    _list = ('/dev/ttyUSB0', '/dev/null')

    return _list

