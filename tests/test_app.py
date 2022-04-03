from unittest import TestCase, skip
from unittest.mock import patch

from api_wrapper.app import app, get_temperature_by_city_name, get_temperature


class TestApp(TestCase):

    def setUp(self):
        self.cached_data = {
            "avg": 280.68,
            "city": {
                "country": "JPN",
                "name": "Tokyo"
            },
            "feels_like": 277.2,
            "max": 281.83,
            "min": 279.59
        }
        self.data = {
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
            }, 'visibility': 10000,
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
    def test_should_return_data_when_city_cached_data_valid(self, mocked_cache):
        """ Should return weather data about specified city when cached data still valid """
        mocked_cache.get.return_value = self.cached_data
        with app.app_context():
            result = get_temperature_by_city_name('tokyo')
            assert result.json['city']['name'] == 'Tokyo'
            assert result.json['city']['country'] == 'JPN'
            assert result.json['min'] == 279.59
            assert result.json['max'] == 281.83
            assert result.json['avg'] == 280.68
            assert result.json['feels_like'] == 277.2

    @patch('api_wrapper.app.support_api')
    @patch('api_wrapper.app.cache')
    def test_should_return_data_from_support_api_when_city_not_cached(self, mocked_cache, mocked_support_api):
        """ Should return weather data from support API when has no cached data """
        mocked_cache.get.return_value = None
        mocked_support_api.get_data_by_city_name.return_value = self.data
        mocked_support_api.get_iso3166_alpha3.return_value = 'JPN'
        with app.app_context():
            result = get_temperature_by_city_name('tokyo')
            assert result.json['city']['name'] == 'Tokyo'
            assert result.json['city']['country'] == 'JPN'
            assert result.json['min'] == 279.59
            assert result.json['max'] == 281.83
            assert result.json['avg'] == 280.68
            assert result.json['feels_like'] == 277.2

    @patch('api_wrapper.app.support_api')
    @patch('api_wrapper.app.cache')
    def test_should_return_error_message_when_city_name_doesnt_exist(self, mocked_cache, mocked_support_api):
        """ Should return error message when city name doesn't exist """
        mocked_cache.get.return_value = None
        mocked_support_api.get_data_by_city_name.return_value = {'cod': '404', 'message': 'city not found'}
        with app.app_context():
            result = get_temperature_by_city_name('t0ky0')
            assert result[0] == {'message': 'city not found'}
            assert result[1] == 404

    @skip
    @patch('api_wrapper.app.cache')
    def test_should_return_only_cities_temperature_max_290(self, mock_cache):
        """ Should return only cities temperatures for up to 290 """
        mock_cache.cache._cache.return_value = {
            "tokyo": {"city": {"name": "Tokyo"}, "max": 281.83},
            "manaus": {"city": {"name": "Manaus"}, "max": 291}
        }
        mock_cache.get.return_value = {"tokyo": 281.83,
                                       "manaus": 291}
        with app.test_request_context('/temperature', data={'max': 290}):
            result = get_temperature()
            assert 'Tokyo' in result.json
            assert 'Manaus' not in result.json
