import json
from urllib2 import urlopen
import requests
from pprint import pprint
from SenseCells.tts import tts
from datetime import datetime, timedelta
import config as cfg
import creds as cr


def get_location():
    url = cfg.IPINFO_URL_API
    response = urlopen(url)
    resp = json.load(response)

    city = resp['city']
    country = resp['country']
    coordinates = resp['loc']

    return city, country, coordinates

def get_weather(day=1):
    city, country, coordinates = get_location()

    lat = coordinates.split(",")[0]
    lon = coordinates.split(",")[1]

    API_key = cr.OPENWEATHERMAP_APY_KEY

    if day == 1:

        try:
            r = requests.get(cr.OWM_LAT_LONG_API_URL.format(lat, lon, API_key))
        except:
            r = requests.get(cr.OWM_CITY_API_URL.format(city, API_key))

        # pprint(r.json())
        weather = r.json()

        temp = weather['main']['temp']
        temp_max = weather['main']['temp_max']
        temp_min = weather['main']['temp_min']
        sunrise = weather['sys']['sunrise']
        sunset = weather['sys']['sunset']
        windspeed = weather['wind']['speed']
        humidity = weather['main']['humidity']

        # # Convert Degree F to Degree C
        # temp = (temp-32)*5/9
        # temp_max = (temp_max - 32) * 5 / 9
        # temp_min = (temp_min - 32) * 5 / 9

        if temp > cfg.SUNNY_WEATHER_LOW_TEMP:
            type_temp = "Sunny"
        elif temp < cfg.CHILLY_WEATHER_HIGH_TEMP:
            type_temp = "Chilly"
        elif temp > cfg.BURNING_WEATHER_LOW_TEMP:
            type_temp = "Burning"
        elif cfg.CHILLY_WEATHER_HIGH_TEMP <= temp <= cfg.SUNNY_WEATHER_LOW_TEMP:
            type_temp = "Pleasant"

        # Convert UTC to datetime
        sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M")
        sunset = datetime.fromtimestamp(sunset).strftime("%H:%M")

        message = "Today is a {} day with temperature of {} degree Celsius. The maximum and minimum temperatures forecasted for today are {} and {} degree Celsius respectively. \
                  The windspeed for today is {} meters per second with a humidity of {} percentage. The sunrise and sunset are forecasted at {} AM and {} PM respectively".format(
                    type_temp, temp, temp_max, temp_min, windspeed, humidity, sunrise, sunset)
        tts(message)

    else:
        day_start = datetime.now().date() - timedelta(days=day)
        day_end = datetime.now().date()

        try:
            r = requests.get(cr.OWM_HISTORY_LAT_LONG_URL.format(lat, lon, API_key, day_start, day_end))
        except:
            r = requests.get(cr.OWM_HISTORY_CITY_URL.format(city, API_key, day_start, day_end))

    pass
