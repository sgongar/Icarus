# coding=utf-8
import ephem
from misc import get_data_from_file

"""
Create a new object each time o change only time?
"""

class Get_data(object):

    def __init__(self):
        """

        """
        location_info = get_data_from_file('.settings')
        observer = self.create_observer(location_info)

        # Return a tuple containing the requested data
        self.get_data(observer)

    def create_observer(self, location_info):
        """ Create observer method
        Method which returns a Observer class object from ephem module

        :param location_info: A list containing the user location
        :return: A Observer class called observer
        """
        observer = ephem.Observer()
        observer.lat = location_info['lat']
        observer.lon = location_info['lon']
        return  observer

    def get_data(self, observer):
        """

        :param timestamp:
        :param observer:
        :return:
        """
        sun = ephem.Sun()
        sun.compute(observer)

        alt, az = sun.alt, sun.az
        return alt, az

