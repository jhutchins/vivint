import logging

from server import Server
from service import Service


logger = logging.getLogger('vivint')


if __name__ == '__main__':
    format = '%(levelname)s\t[%(asctime)s]'
    format += ' [%(pathname)s:%(lineno)d] %(message)s'
    logging.basicConfig(format=format, level=logging.DEBUG)
    Server(Service()).run()
    logger.info('Shutdown')
