import argparse

from api_wrapper import create_app
from api_wrapper.conf.dev import DevConf

parser = argparse.ArgumentParser(description='It\'s a wrapper of Open Weather API.')
parser.add_argument('--port', dest='port', default=5000, help='The port of the webserver')
parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False,
                    help='Enable or disable debug mode')

app = create_app(DevConf)

if __name__ == '__main__':
    args = parser.parse_args()
    app.run(port=args.port, debug=args.debug)
