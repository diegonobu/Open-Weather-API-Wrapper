import os

import requests
from flask import Flask, request, jsonify
from flask_caching import Cache

from api_wrapper.models import Weather

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
    weather = Weather.convert(r.json())
    cache.set(city_name, weather.dict())
    return jsonify(weather.dict())


@app.route('/temperature')
def get_temperature():
    max = request.args.get('max', float(default_max_number), float)
    max_of_cities = {city_name: cache.get(city_name)['max']
                     for city_name in cache.cache._cache
                     if cache.get(city_name)['max'] <= max}

    return jsonify(max_of_cities)
