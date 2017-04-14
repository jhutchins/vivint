class ServiceError(Exception):
    pass


class ReadonlyError(ServiceError):

    def __init__(self, name):
        self.name = name
        self.message = 'value is readonly'


class UnknownAttributeError(ServiceError):

    def __init__(self, name):
        self.name = name
        self.message = 'unknown attribute'


class UnknownThermostatError(ServiceError):

    def __init__(self, id):
        self.name = id
        self.message = 'unknown thermostat {}'.format(id)


class ValidationError(ServiceError):

    def __init__(self, name, message):
        self.name = name
        self.message = message
