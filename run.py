import argparse

from api_wrapper.app import app, cache

parser = argparse.ArgumentParser(description='It\'s a wrapper of Open Weather API.')
parser.add_argument('--port', dest='port', default=5000, help='The port of the webserver')
parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False,
                    help='Enable or disable debug mode')

if __name__ == '__main__':
    cache.init_app(app)
    args = parser.parse_args()
    app.run(port=args.port, debug=args.debug)
