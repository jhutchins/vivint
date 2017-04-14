import json
import logging
import web

from errors import (ReadonlyError, ServiceError, UnknownAttributeError,
                    UnknownThermostatError, ValidationError)
from service import Service


logger = logging.getLogger(__name__)


class Thermostats:
    """Handle requests at the level of all thermostats"""

    def GET(self):
        """Return all data about all known thermostats

        The response will be returned in JSON format and will contain all
        information currently known to the system about all thermostats.
        """
        web.header('Content-Type', 'application/json')
        result = json.dumps({'result': service.thermostats()})
        logger.debug('result = {}', result)
        return result


class Thermostat:
    """Handle requests at the level of an individual thermostat."""

    def GET(self, id):
        """Retrieve all known data about a thermostat.

        All known information for a thermostat will be returned in JSON
        format. If the thermostat indicated by the id cannot be found a
        not found response will be returned.
        """
        try:
            result = service.thermostat(id)
            web.header('Content-Type', 'application/json')
            result = json.dumps({'result': result})
            logger.debug('result = {}', result)
            return result
        except UnknownThermostatError:
            logger.warn('request for unknown thermostat {}'.format(id))
            return web.notfound()

    def PATCH(self, id):
        """Modify a set of attributes on a particular thermostat.

        The group of attributes should be a JSON object containing a
        attribute name and value mapping. The response will be a JSON
        object with the attribute names and the result of each individual
        change operation. If the change was sucessful the value will be 'ok',
        otherwise the value will be an informative explination of why the
        change could not be made.

        Failure to identify the indicated thermostate will result in a not
        found response.

        A request payload that is not valid json or is something other than
        a JSON object will result in a bad request response.
        """
        data = web.data()
        try:
            value = json.loads(data)
        except ValueError:
            logger.warn('request payload was invalid JSON: {}'.format(data))
            # Not valid JSON
            return web.badrequest()
        if not isinstance(value, dict):
            logger.warn('request payload not a JSON object: {}'.format(value))
            return web.badrequest()

        result = {}

        for k, v in value.items():
            try:
                service.set_attribute(id, k, v)
                result[k] = 'ok'
            except UnknownThermostatError:
                return web.notfound()
            except ServiceError as e:
                result[k] = e.message
        web.header('Content-Type', 'application/json')
        result = json.dumps({'result': result})
        logger.debug('result = {}'.format(result))
        return result


class Attribute:
    """Handle requests at the level of individual attriubtes"""

    def GET(self, id, name):
        """Retrieve an attribute.

        This will return the value of an attribute in JSON format.
        Failure to location the specified thermostat or attribute
        will result in an appropriate not found response.
        """
        try:
            result = service.get_attribute(id, name)
            web.header('Content-Type', 'application/json')
            result = json.dumps({'result': result})
            logger.debug('result = {}'.format(result))
            return result
        except (UnknownAttributeError, UnknownThermostatError) as e:
            if isinstance(e, UnknownAttributeError):
                logger.warn('request for unknown attribute {}'.format(name))
            else:
                logger.warn('request for unknown thermostat {}'.format(id))
            return web.notfound()

    def PUT(self, id, name):
        """Modify the value of the indicated attribute.

        The payload of the request must be in JSON format and be either
        a string or an interger depending on the expected value of the
        indicated attribute.

        If the payload is not in JSON format a bad request will be returned.

        If the attrubte cannot be modified, for example the id attribute,
        than a forbidden response will be returned.

        Inability to locate the indicated thermostat or attribute will
        result in a not found response.

        In the case of success the response will be not content.
        """
        # TODO add a text/plain API
        data = web.data()
        try:
            value = json.loads(data)
            service.set_attribute(id, name, value)
            logger.debug('value set')
            return web.nocontent()
        except (ValidationError, ValueError) as e:
            if isinstance(e, ValidationError):
                msg = 'got invalid value ({}) for {}; {}'
                logger.warn(msg.format(value, name, e.message))
            else:
                logger.warn('got invalid JSON payload: {}'.format(data))
            return web.badrequest()
        except ReadonlyError:
            logger.warn('got request to change readonly value {}'.format(name))
            return web.forbidden()
        except (UnknownAttributeError, UnknownThermostatError) as e:
            if isinstance(e, UnknownAttributeError):
                msg = 'request to set value for unkown attribute {}'
                logger.warn(msg.format(name))
            else:
                msg = 'request to set value for unknown thermostat {}'
                logger.warn(msg.format(id))
            return web.notfound()


def redirect_to_slash(handler):
    """Redirect request if not ending in '/'

    A request to a path not ending will receive a redirect request to
    the same path, but with a slash append.
    """
    path = web.webapi.ctx.env['PATH_INFO']
    logger.debug('request to path: {}'.format(path))
    if path is not None and path[-1] != '/':
        return web.redirect(path + '/')
    return handler()


def require_json(handler):
    """Reject payload requests not in json

    Requests with PUT or PATCH methods will be required to include a
    Content-Type header with the value of application/json. Requests
    without the header will receive a bad request response. Those with
    a value other than application/json will receive a unsupported
    media type response.
    """
    env = web.webapi.ctx.env
    method = env['REQUEST_METHOD']
    if method == 'PUT' or method == 'PATCH':
        if 'CONTENT_TYPE' not in env:
            logger.warn('{} request without Content-Type'.format(method))
            return web.badrequest()
        content_type = env['CONTENT_TYPE']
        if not content_type.startswith('application/json'):
            msg = '{} request with Content-Type of {}'
            logger.warn(msg.format(method, content_type))
            return web.unsupportedmediatype()
    return handler()


class Server:
    """A class to expose a RESTful API to thermostats

    This class handles all web related aspects of the API, ie
    (de)serializing JSON, converting responses to HTTP codes,
    checking Content-Type, etc. The acutal communication with
    the thermostats is preformed by the Service class.

    This object can also be stated to expose a web server.
    """

    def __init__(self, service):
        """Create a new web server

        Requires a service to be provided to which the commnunication
        with the thermostats will be deligated.
        """
        logger.debug('initializing web service')
        urls = (
            '/thermostats/', Thermostats,
            '/thermostats/(\w+)/', Thermostat,
            '/thermostats/(\w+)/([^/]+)/', Attribute,
        )
        env = globals()
        env['service'] = service
        self.app = web.application(urls, env)
        self.app.add_processor(redirect_to_slash)
        self.app.add_processor(require_json)

    def run(self):
        """Start the web server"""
        self.app.run()
