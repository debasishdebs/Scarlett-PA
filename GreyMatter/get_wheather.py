import json
from urllib2 import urlopen
import requests
from pprint import pprint
from SenseCells.tts import tts
from datetime import datetime, timedelta
import config as cfg
import creds as cr


class GetWeather(object):
    def __init__(self, DAY=1):
        self.OWM_LAT_LONG_API_URL = cr.OWM_LAT_LONG_API_URL
        self.OWM_CITY_API_URL = cr.OWM_CITY_API_URL
        self.API_KEY = cr.OPENWEATHERMAP_APY_KEY
        self.OWM_HISTORY_LAT_LONG_API_URL = cr.OWM_HISTORY_LAT_LONG_URL
        self.OWM_HISTORY_CITY_API_URL = cr.OWM_HISTORY_CITY_URL
        self.IPINFO_URL = cfg.IPINFO_URL_API

        self.day = DAY

        self.t1 = cfg.CHILLY_WEATHER_HIGH_TEMP
        self.t2 = cfg.SUNNY_WEATHER_LOW_TEMP
        self.t3 = cfg.BURNING_WEATHER_LOW_TEMP
        pass

    def __driver__(self):
        self.city, self.country, self.coordinates = self.get_location()
        self.get_weather()
        pass

    def get_location(self):
        url = self.IPINFO_URL
        response = urlopen(url)
        resp = json.load(response)

        city = resp['city']
        country = resp['country']
        coordinates = resp['loc']

        return city, country, coordinates

    def get_weather(self):
        city, country, coordinates = self.city, self.country, self.coordinates

        lat = coordinates.split(",")[0]
        lon = coordinates.split(",")[1]

        API_key = self.API_KEY

        if self.day == 1:

            try:
                r = requests.get(self.OWM_LAT_LONG_API_URL.format(lat, lon, API_key))
            except:
                r = requests.get(self.OWM_CITY_API_URL.format(city, API_key))

            weather = r.json()

            temp = weather['main']['temp']
            temp_max = weather['main']['temp_max']
            temp_min = weather['main']['temp_min']
            sunrise = weather['sys']['sunrise']
            sunset = weather['sys']['sunset']
            windspeed = weather['wind']['speed']
            humidity = weather['main']['humidity']

            if temp > self.t2:
                type_temp = "Sunny"
            elif temp < self.t1:
                type_temp = "Chilly"
            elif temp > self.t3:
                type_temp = "Burning"
            elif self.t1 <= temp <= self.t2:
                type_temp = "Pleasant"

            # Convert UTC to datetime
            sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M")
            sunset = datetime.fromtimestamp(sunset).strftime("%H:%M")

            message = "Today is a {} day with temperature of {} degree Celsius. The maximum and minimum \
                            temperatures forecasted for today are {} and {} degree Celsius respectively. \
                          The windspeed for today is {} meters per second with a humidity of {} percentage. \
                          The sunrise and sunset are forecasted at {} AM and {} PM respectively".format(
                type_temp, temp, temp_max, temp_min, windspeed, humidity, sunrise, sunset)
            tts(message)

        else:
            day_start = datetime.now().date() - timedelta(days=self.day)
            day_end = datetime.now().date()

            try:
                r = requests.get(self.OWM_HISTORY_LAT_LONG_API_URL.format(lat, lon, API_key, day_start, day_end))
            except:
                r = requests.get(self.OWM_HISTORY_CITY_API_URL.format(city, API_key, day_start, day_end))
        pass
