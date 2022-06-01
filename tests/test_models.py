from api_wrapper import models

DATA = {
    'coord': {'lon': -121.9358, 'lat': 37.7021},
    'weather': [
        {'id': 800,
         'main': 'Clear',
         'description': 'clear sky',
         'icon': '01d'}
    ],
    'base': 'stations',
    'main': {
        'temp': 295.76,
        'feels_like': 295.17,
        'temp_min': 289.59,
        'temp_max': 299.45,
        'pressure': 1010,
        'humidity': 42
    },
    'visibility': 10000,
    'wind': {'speed': 5.14, 'deg': 280},
    'clouds': {'all': 0},
    'dt': 1648946900,
    'sys': {
        'type': 2,
        'id': 2016191,
        'country': 'US',
        'sunrise': 1648907474,
        'sunset': 1648953056
    },
    'timezone': -25200,
    'id': 5344157,
    'name': 'Dublin',
    'cod': 200
}


def test_should_set_right_city_name_and_country_name():
    """ Should set right values for 'name' and 'country' """
    city = models.City.convert(DATA)

    assert city.name == 'Dublin'
    assert city.country == 'USA'


def test_should_set_right_max_min_avg_feels_like_and_city():
    """ Should set right values for 'max', 'min', 'avg', 'feels_like' and 'city' """
    weather = models.Weather.convert(DATA)

    assert weather.city.name == 'Dublin'
    assert weather.city.country == 'USA'
    assert weather.max == 299.45
    assert weather.min == 289.59
    assert weather.avg == 295.76
    assert weather.feels_like == 295.17
