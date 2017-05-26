import json
from urllib2 import urlopen
import requests
from pprint import pprint
from SenseCells.tts import tts
from datetime import datetime, timedelta


def get_location():
    url = "http://ipinfo.io/json"
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

    API_key = "a00f94d85e7a9c5518446eb5f1b3ce21"

    if day == 1:

        try:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}&units=metric'.format(lat, lon, API_key))
        except:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric'.format(city, API_key))

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

        if temp > 25:
            type_temp = "Sunny"
        elif temp < 15:
            type_temp = "Chilly"
        elif temp > 35:
            type_temp = "Burning"
        elif temp >= 15 and temp <= 25:
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
            r = requests.get('http://history.openweathermap.org/data/2.5/history/city?\
                            lat={}&lon={}&type=daily&APPID={}&units=metric&start={}&end={}'.format(lat, lon, API_key, day_start, day_end))
        except:
            r = requests.get('http://history.openweathermap.org/data/2.5/history/city?\
                            q={}&APPID={}&units=metric&type=daily&start={}&end={}'.format(city, API_key, day_start, day_end))

    pass