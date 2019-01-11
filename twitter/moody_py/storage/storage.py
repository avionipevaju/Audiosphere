import logging

import redis


class Redis:
    """
    Enables connection to Redis data storage and provides basic operation on it
    """

    YAHOO_WEATHER_CODE = 'yahoo:weather:code:{}'
    TIME_OF_DAY_CONTENT = 'time:content:{}'

    def __init__(self):
        self.redis_engine = redis.StrictRedis(host='moody_sense', port=6380, db=0)

    def get_string(self, key):
        """
        Gets the string for a given key
        :param key: Key to search by
        :return: String value for a given key or None if it doesn't exist
        """
        return self.redis_engine.get(key)

    def get_list(self, key):
        """
        Gets the list for a given key
        :param key: Key to search by
        :return: List of values for a given key or None if the list doesn't exist
        """
        redis_list = self.redis_engine.lrange(key, 0, -1)
        if redis_list is None:
            logging.error('No genres for code: %s', key)
            raise Exception('Genre list is None')
        return redis_list

    def get_genre_list(self, condition_code):
        """
        Get a full list of genres based on the weather data
        :param condition_code: Code representing the current weather
        :return:list of genres corresponding to the weather data
        """
        return self.get_list(self._assemble_search_key(self.YAHOO_WEATHER_CODE, condition_code))

    def get_time_of_day_content_list(self, time_of_day):
        """
        Get a full list of content based on the weather data time of day
        :param time_of_day: Specifies what time of day it is
        :return:list of content corresponding to the weather data time of day
        """
        return self.get_list(self._assemble_search_key(self.TIME_OF_DAY_CONTENT, time_of_day))

    @staticmethod
    def _assemble_search_key(base, key):
        return base.format(key)
