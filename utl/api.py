import urllib.request as request
import json

def getCurrentWeather():
    weatherlink = "https://www.metaweather.com/api/location/2459115/"
    weatherjson = request.urlopen(weatherlink).read()
    weather = json.loads(weatherjson)['consolidated_weather'][0]
    weather['min_temp'] = int(weather['min_temp'] * 9.0 / 5.0 + 32)
    weather['max_temp'] = int(weather['max_temp'] * 9.0 / 5.0 + 32)
    weather['the_temp'] = int(weather['the_temp'] * 9.0 / 5.0 + 32)
    return weather

def getNewsArticles():
     newslink = "https://newsapi.org/v2/top-headlines?country=us&apiKey=0eb326895bb344acb80c48b0a3338c7b"
     newsjson = request.urlopen(newslink).read()
     news = json.loads(newsjson)['articles']
     print(news)
     return news

