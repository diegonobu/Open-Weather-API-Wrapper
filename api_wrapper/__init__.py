from flask import Flask

from api_wrapper.app import cache, temperature


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(temperature)
    cache.init_app(app)
    return app
