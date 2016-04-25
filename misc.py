# coding=utf-8
from os import path, getcwd
from configparser import ConfigParser, SafeConfigParser


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

    return st
