import json
import web

from errors import (ReadonlyError, ServiceError, UnknownAttributeError,
                    UnknownThermostatError, ValidationError)
from service import Service


class Thermostats:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps({'result': service.thermostats()})


class Thermostat:
    def GET(self, id):
        try:
            result = service.thermostat(id)
            web.header('Content-Type', 'application/json')
            return json.dumps({'result': result})
        except UnknownThermostatError:
            return web.notfound()

    def PATCH(self, id):
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
    def GET(self, id, name):
        try:
            result = service.get_attribute(id, name)
            web.header('Content-Type', 'application/json')
            return json.dumps({'result': result})
        except (UnknownAttributeError, UnknownThermostatError):
            return web.notfound()

    def PUT(self, id, name):
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

    def __init__(self, service):
        urls = (
            '/thermostats/?', Thermostats,
            '/thermostats/(\w+)/?', Thermostat,
            '/thermostats/(\w+)/([^/]+)/?', Attribute,
        )
        env = globals()
        env['service'] = Service()
        self.app = web.application(urls, env)

    def run(self):
        self.app.run()
