from unittest.mock import MagicMock

import pytest
from icontract.errors import ViolationError

from api_wrapper import support_api


def test_get_iso3166_alpha3():
    """ Should success """
    support_api.get_iso3166_alpha3('JP')


def test_get_iso3166_alpha3_raise_pre_violation_error():
    """ Raise ViolationError because pre data length should be 2 """
    with pytest.raises(ViolationError) as err:
        support_api.get_iso3166_alpha3('JPN')

    assert 'country code must have 2 letters' in err.value.args[0]


def test_get_iso3166_alpha3_raise_post_violation_error():
    """ Raise ViolationError because post data length should be 3 """
    mock_requests = MagicMock()
    mock_get = MagicMock()
    support_api.requests = mock_requests
    mock_requests.get = MagicMock(return_value=mock_get)
    mock_get.json.return_value = None, [{'id': 'JP'}]

    with pytest.raises(ViolationError) as err:
        support_api.get_iso3166_alpha3('JP')

    assert 'country code of result must have 3 letters' in err.value.args[0]
