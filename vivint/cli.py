import argparse
import logging
import vivint
import sys

from server import Server
from service import Service


logger = logging.getLogger('vivint')


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser(description='Run thermostat web service')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(vivint.__version__))
    parser.add_argument('--log', dest='loglevel', default='info',
                        help='log level (default: info)')
    parser.add_argument('port', nargs='?', action='store', default=8080,
                        help='web server port (defaul: 8080)')
    args = parser.parse_args()

    # Setup logging
    format = '%(levelname)s\t[%(asctime)s]'
    format += ' [%(pathname)s:%(lineno)d] %(message)s'
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format=format, level=numeric_level)

    # Hack because web.py is a huge idiot
    port = str(args.port)
    if len(sys.argv) < 2:
        sys.argv.append(port)
    else:
        sys.argv[1] = port

    # Run web server
    Server(Service()).run()
    logger.info('Shutdown')
