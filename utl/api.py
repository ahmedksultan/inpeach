import urllib.request as request
import json

def getCurrentWeather():
    weatherlink = "https://www.metaweather.com/api/location/2459115/"
    weatherjson = request.urlopen(weatherlink).read()
    weather = json.loads(weatherjson)['consolidated_weather'][0]
    weather['min_temp'] = weather['min_temp'] * 9.0 / 5.0 + 32
    weather['max_temp'] = weather['max_temp'] * 9.0 / 5.0 + 32
    weather['the_temp'] = weather['the_temp'] * 9.0 / 5.0 + 32
    return weather