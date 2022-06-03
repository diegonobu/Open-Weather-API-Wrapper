import pytest

from api_wrapper import create_app
from api_wrapper.conf.testing import TestConf


@pytest.fixture()
def app():
    app = create_app(TestConf)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
