import os

import requests
from flask import Flask, request, jsonify
from flask_caching import Cache

from models import Weather, City

app = Flask(__name__)
cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
})

API_URL = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
default_max_number = os.environ.get('DEFAULT_MAX_NUMBER')


@app.route('/temperature/<string:city_name>')
def get_temperature_by_city_name(city_name):
    city_weather = cache.get(city_name)
    if city_weather:
        return jsonify(city_weather)

    params = {'q': city_name, 'appid': API_KEY}
    r = requests.get(API_URL, params=params)
    data = r.json()
    city = City(name=data['name'], country=data['sys']['country'])
    main_ = data['main']
    weather = Weather(min=main_['temp_min'],
                      max=main_['temp_max'],
                      avg=main_['temp'],
                      feels_like=main_['feels_like'],
                      city=city)
    cache.set(city_name, weather.dict())
    return jsonify(weather.dict())


@app.route('/temperature')
def get_temperature():
    max = request.args.get('max', float(default_max_number), float)
    max_of_cities = {}
    for city_name in cache.cache._cache:
        city = cache.get(city_name)
        if city['max'] <= max:
            max_of_cities[city_name] = city['max']

    return jsonify(max_of_cities)
