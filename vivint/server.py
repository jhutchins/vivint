import json
import web

from service import Service

# TODO I'm not crazy about this global variable
SERVICE = Service()


class Thermostats:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return SERVICE.thermostats()


class Thermostat:
    def GET(self, id):
        result = SERVICE.thermostat(id)
        if result is None:
            return web.notfound()
        web.header('Content-Type', 'application/json')
        return result


class Attribute:
    def GET(self, id, name):
        result = SERVICE.get_attribute(id, name)
        if result is None:
            return web.notfound()
        web.header('Content-Type', 'application/json')
        # Make sure that returned strings are quoted JSON strings
        return json.dumps(result)

    def PUT(self, id, name):
        value = web.data()
        result = SERVICE.set_attribute(id, name, value)
        if result is None:
            return web.notfound()
        if not result:
            return web.badrequest()
        return web.nocontent()


def run():
    urls = (
        '/thermostats/?', Thermostats,
        '/thermostats/(\w+)/?', Thermostat,
        '/thermostats/(\w+)/(.+)/?', Attribute,
    )
    app = web.application(urls, globals())
    app.run()
