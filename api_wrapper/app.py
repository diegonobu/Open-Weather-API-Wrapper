import os

from flask import Flask, request, jsonify
from flask_caching import Cache

from api_wrapper import support_api
from api_wrapper.models import Weather

app = Flask(__name__)
cache = Cache(config={
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', default='SimpleCache'),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', default=300)),
    'CACHE_THRESHOLD': int(os.environ.get('CACHE_THRESHOLD', default=5))
})

default_max_number = int(os.environ.get('DEFAULT_MAX_NUMBER', default=290))


@app.route('/temperature/<string:city_name>')
def get_temperature_by_city_name(city_name):
    """
    Gets description of weather of queried city.

    :param (str) city_name: Name of the city.
    :return: Weather data in JSON format.
    """
    city_weather = cache.get(city_name)
    if city_weather:
        return jsonify(city_weather)

    city_data = support_api.get_data_by_city_name(city_name)
    if city_data['cod'] == '404':
        return {'message': city_data['message']}, 404

    weather = Weather.convert(city_data)
    weather.city.country = support_api.get_iso3166_alpha3(weather.city.country)
    cache.set(city_name, weather.dict())
    return jsonify(weather.dict())


@app.route('/temperature')
def get_temperature():
    """
    Gets list of cached cities with max temperature.

    :return: List of cached cities with max temperature.
    """
    max_ = request.args.get('max', float(default_max_number), float)
    max_of_cities = {city_name: cache.get(city_name)['max']
                     for city_name in cache.cache._cache
                     if cache.get(city_name)['max'] <= max_}

    return jsonify(max_of_cities)
