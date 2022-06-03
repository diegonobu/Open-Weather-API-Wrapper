from unittest.mock import patch


CACHED_DATA = {
    "avg": 280.68,
    "city": {
        "country": "JPN",
        "name": "Tokyo"
    },
    "feels_like": 277.2,
    "max": 281.83,
    "min": 279.59
}
RESPONSE_DATA = {
    'coord': {
        'lon': 139.6917, 'lat': 35.6895},
    'weather': [
        {
            'id': 803,
            'main': 'Clouds',
            'description': 'broken clouds',
            'icon': '04n'
        }
    ],
    'base': 'stations',
    'main': {
        'temp': 280.68,
        'feels_like': 277.2,
        'temp_min': 279.59,
        'temp_max': 281.83,
        'pressure': 1028,
        'humidity': 92
    },
    'visibility': 10000,
    'wind': {'speed': 6.17, 'deg': 320},
    'clouds': {'all': 75},
    'dt': 1649003979,
    'sys': {
        'type': 2,
        'id': 2038398,
        'country': 'JP',
        'sunrise': 1649017448,
        'sunset': 1649063055
    },
    'timezone': 32400,
    'id': 1850144,
    'name': 'Tokyo',
    'cod': 200
}


@patch('api_wrapper.app.cache')
def test_should_return_data_when_city_cached_data_valid(mocked_cache, client):
    """ Should return weather data about specified city when cached data still valid """
    mocked_cache.get.return_value = CACHED_DATA

    response = client.get("/temperature/tokyo")

    assert response.json['city']['name'] == 'Tokyo'
    assert response.json['city']['country'] == 'JPN'
    assert response.json['min'] == 279.59
    assert response.json['max'] == 281.83
    assert response.json['avg'] == 280.68
    assert response.json['feels_like'] == 277.2


@patch('api_wrapper.app.support_api')
@patch('api_wrapper.app.cache')
def test_should_return_data_from_support_api_when_city_not_cached(mocked_cache, mocked_support_api, client):
    """ Should return weather data from support API when has no cached data """
    mocked_cache.get.return_value = None
    mocked_support_api.get_data_by_city_name.return_value = RESPONSE_DATA
    mocked_support_api.get_iso3166_alpha3.return_value = 'JPN'

    response = client.get("/temperature/tokyo")

    assert response.json['city']['name'] == 'Tokyo'
    assert response.json['city']['country'] == 'JPN'
    assert response.json['min'] == 279.59
    assert response.json['max'] == 281.83
    assert response.json['avg'] == 280.68
    assert response.json['feels_like'] == 277.2


@patch('api_wrapper.app.support_api')
@patch('api_wrapper.app.cache')
def test_should_return_error_message_when_city_name_doesnt_exist(mocked_cache, mocked_support_api, client):
    """ Should return error message when city name doesn't exist """
    mocked_cache.get.return_value = None
    mocked_support_api.get_data_by_city_name.return_value = {'cod': '404', 'message': 'city not found'}

    response = client.get("/temperature/tokyo")

    assert response.json == {'message': 'city not found'}
    assert response.status_code == 404


@patch('api_wrapper.app.support_api')
@patch('api_wrapper.app.cache')
def test_example_of_pre_usage(mocked_cache, mocked_support_api, client):
    """ Should raise a ViolationError because pre data of 'country' length is not 3 """
    mocked_cache.get.return_value = None
    RESPONSE_DATA['sys']['country'] = 'JPN'
    mocked_support_api.get_data_by_city_name.return_value = RESPONSE_DATA

    client.get("/temperature/tokyo")


@patch('api_wrapper.app.support_api')
@patch('api_wrapper.app.cache')
def test_example_of_post_usage(mocked_cache, mocked_support_api, client):
    """ Should raise a ViolationError because post data of 'country' length is not 2 """
    mocked_cache.get.return_value = None
    RESPONSE_DATA['sys']['country'] = 'JP'
    mocked_support_api.get_data_by_city_name.return_value = RESPONSE_DATA
    mocked_support_api.get_iso3166_alpha3.return_value = 'JP'

    client.get("/temperature/tokyo")
