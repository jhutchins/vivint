import json
import web

from errors import (ReadonlyError, ServiceError, UnknownAttributeError,
                    UnknownThermostatError, ValidationError)
from service import Service


class Thermostats:
    """Handle requests at the level of all thermostats"""

    def GET(self):
        """Return all data about all known thermostats

        The response will be returned in JSON format and will contain all
        information currently known to the system about all thermostats.
        """
        web.header('Content-Type', 'application/json')
        return json.dumps({'result': service.thermostats()})


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
            return json.dumps({'result': result})
        except UnknownThermostatError:
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
        try:
            value = json.loads(web.data())
        except ValueError:
            # Not valid JSON
            return web.badrequest()
        if not isinstance(value, dict):
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
        return json.dumps({'result': result})


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
            return json.dumps({'result': result})
        except (UnknownAttributeError, UnknownThermostatError):
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
        try:
            value = json.loads(web.data())
            result = service.set_attribute(id, name, value)
            return web.nocontent()
        except (ValidationError, ValueError):
            return web.badrequest()
        except ReadonlyError:
            return web.forbidden()
        except (UnknownAttributeError, UnknownThermostatError):
            return web.notfound()


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
        with the thermostats will be delicated.
        """
        urls = (
            '/thermostats/?', Thermostats,
            '/thermostats/(\w+)/?', Thermostat,
            '/thermostats/(\w+)/([^/]+)/?', Attribute,
        )
        env = globals()
        env['service'] = Service()
        self.app = web.application(urls, env)

    def run(self):
        """Start the web server"""
        self.app.run()
