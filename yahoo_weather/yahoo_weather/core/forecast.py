import logging
import os

from weather import Weather, Unit

from yahoo_weather.core.model import WeatherData


class Forecast:
    """
    Provides forecast information for a given location by using Yahoo Weather API.
    """

    def __init__(self, city, unit=Unit.CELSIUS):
        """
        Initializes the Forecast engine with settings for a given city and temperature unit
        :param city: City of interest
        :param unit: Temperature unit
        """
        logging.info('Configuring forecast data for %s in %s', city, unit)
        if os.environ['enable_mock'] == 'False':
            self.weather = Weather(unit=unit)
        self.city = city

    def current_weather(self):
        """
        Gets the current forecast for a city
        :return: Weather Data representing the current forecast of a city
        """
        if os.environ['enable_mock'] == 'True':
            weather_data = WeatherData(None)
            weather_data.location = self.city
        else:
            weather_data = WeatherData(self.weather.lookup_by_location(self.city))
        logging.info('Retrieved current forecast for %s %s', self.city, weather_data)
        return weather_data
