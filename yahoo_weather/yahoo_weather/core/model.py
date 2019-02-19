import datetime


class WeatherData:
    """
    Data transfer object containing relevant forecast data
    """

    _to_string = 'Location: {}, Condition: {}, Condition Code: {}, Temperature: {}, Date: {}, Time: {}, {}'

    def __init__(self, weather_object):
        """
        Weather data assembler
        :param weather_object: Yahoo Weather weather_object
        """
        if weather_object is None:
            self.create_mock_response()
        else:
            self.location = self.resolve_location(weather_object.description)
            self.condition = weather_object.condition.text
            self.condition_code = weather_object.condition.code
            self.temperature = weather_object.condition.temp
            self.date = weather_object.condition.date
            # TODO Change time and time of day not to be local but to depend on the location and the timezone
            self.time = datetime.datetime.time(datetime.datetime.now())
            self.time_of_day = self.get_time_of_day()

    def create_mock_response(self):
        """
        Creates a mock response from YahooWeather server because of temporary unavailable service.
        :param location:
        :return:
        """
        self.condition = 'Sunny'
        self.condition_code = 12
        self.temperature = 'N/A'
        self.time = datetime.datetime.time(datetime.datetime.now())
        self.date = self.time.strftime('%d/%m/%Y')
        self.time_of_day = self.get_time_of_day()

    @staticmethod
    def resolve_location(yahoo_description):
        """
        Extracts the location from Yahoo forecast description
        :param yahoo_description: Yahoo forecast description
        :return: Location name
        """
        return yahoo_description.split(" ")[4][:-1]

    def get_time_of_day(self):
        hour = self.time.hour
        if 6 <= hour < 11:
            return TimeOfDay.MORNING
        if 11 <= hour < 17:
            return TimeOfDay.DAY
        if 17 <= hour < 20:
            return TimeOfDay.EVENING
        if 20 <= hour < 24 or 0 <= hour < 6:
            return TimeOfDay.NIGHT

    def __str__(self):
        return self._to_string.format(self.location, self.condition, self.condition_code, self.temperature, self.date,
                                      self.time, self.time_of_day)


class TimeOfDay:
    """
    Value object representing time of day
    """

    MORNING = "Morning"
    DAY = "Day"
    EVENING = "Evening"
    NIGHT = "Night"

    def __init__(self):
        pass
