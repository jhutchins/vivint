from errors import (ReadonlyError, UnknownAttributeError,
                    UnknownThermostatError, ValidationError)


class Service:
    """A service to handle communication with the thermostats

    This version of the service is an in memory stub mock but could be
    replaced or updated to actually communication with real thermostats.
    """

    FAN_MODES = {u'auto', u'on'}
    OPERATING_MODES = {u'cool', u'heat', u'off'}

    def __init__(self):
        """Create a new service"""
        self._data = {
            100: {
                'id': 100,
                'name': 'Upstairs Thermostat',
                'current-temp': 71,
                'operating-mode': 'heat',
                'cool-setpoint': 75,
                'heat-setpoint': 65,
                'fan-mode': 'auto'
            },
            101: {
                'id': 101,
                'name': 'Downstairs Thermostat',
                'current-temp': 69,
                'operating-mode': 'heat',
                'cool-setpoint': 75,
                'heat-setpoint': 65,
                'fan-mode': 'auto'
            }
        }
        self.validators = {
            'name': self._name_validation,
            'operating-mode': self._operating_mode_validation,
            'cool-setpoint': self._cool_setpoint_validation,
            'heat-setpoint': self._heat_setpoint_validation,
            'fan-mode': self._fan_mode_validation,
        }

    def thermostats(self):
        """Return information about all known thermostats.

        >>> Service().thermostats()
        [{'name': 'Upstairs Thermostat', 'operating-mode': 'heat', 'cool-setpoint': 75, 'heat-setpoint': 65, 'fan-mode': 'auto', 'current-temp': 71, 'id': 100}, {'name': 'Downstairs Thermostat', 'operating-mode': 'heat', 'cool-setpoint': 75, 'heat-setpoint': 65, 'fan-mode': 'auto', 'current-temp': 69, 'id': 101}]
        """
        return self._data.values()

    def thermostat(self, id):
        """Return information about a specific thermostat.

        If the id matches a managed thermostat the related data will be
        returned

        >>> Service().thermostat(100)
        {'name': 'Upstairs Thermostat', 'operating-mode': 'heat', 'cool-setpoint': 75, 'heat-setpoint': 65, 'fan-mode': 'auto', 'current-temp': 71, 'id': 100}


        If the provided id attribute is unknown then an
        UnknownThermostatError will be raised instead.

        >>> Service().thermostat(102)
        Traceback (most recent call last):
        ...
        UnknownThermostatError

        >>> Service().thermostat('sdf')
        Traceback (most recent call last):
        ...
        UnknownThermostatError
        """
        try:
            return self._data[int(id)]
        except (ValueError, KeyError):
            raise UnknownThermostatError(id)

    def get_attribute(self, id, name):
        """Return the value for a named attribute

        >>> Service().get_attribute(100, 'name')
        'Upstairs Thermostat'


        If the id doesn't match a known thermostat an
        UnknownThermostatError will be raised.

        >>> Service().get_attribute(102, 'name')
        Traceback (most recent call last):
        ...
        UnknownThermostatError


        If the name doesn't reference a know attribute than an
        UnknownAttributeError will be raised

        >>> Service().get_attribute(100, 'size')
        Traceback (most recent call last):
        ...
        UnknownAttributeError
        """
        try:
            return self.thermostat(id)[name]
        except KeyError:
            raise UnknownAttributeError(name)

    def set_attribute(self, id, name, value):
        """Set the attribute for an identified thermostat

        >>> service = Service()
        >>> service.set_attribute(100, 'name', 'New Name')
        >>> service.get_attribute(100, 'name')
        'New Name'


        If the id doesn't match a known thermostat an
        UnknownThermostatError will be raised.

        >>> Service().set_attribute(102, 'name', 'New Name')
        Traceback (most recent call last):
        ...
        UnknownThermostatError


        If the name doesn't reference a know attribute than an
        UnknownAttributeError will be raised

        >>> Service().set_attribute(100, 'size', 45)
        Traceback (most recent call last):
        ...
        UnknownAttributeError


        If the name references a read-only attribute a
        ReadonlyError will be raised

        >>> Service().set_attribute(100, 'current-temp', 80)
        Traceback (most recent call last):
        ...
        ReadonlyError


        And finally if the value is invalid in some way a
        ValidationError will be raised

        >>> Service().set_attribute(100, 'fan-mode', 'high')
        Traceback (most recent call last):
        ...
        ValidationError
        """
        thermostat = self.thermostat(id)
        if name not in thermostat:
            raise UnknownAttributeError(name)

        try:
            self.validators[name](value)
        except KeyError:
            raise ReadonlyError(name)

        thermostat[name] = value

    ########################
    #  VALIDATION METHODS  #
    ########################

    def _name_validation(self, value):
        if not isinstance(value, basestring) or value == '':
            raise ValidationError('name', 'value cannot be blank')

    def _cool_setpoint_validation(self, value):
        self._validate_setpoint('cool-setpoint', value)

    def _heat_setpoint_validation(self, value):
        self._validate_setpoint('heat-setpoint', value)

    def _validate_setpoint(self, name, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(name, 'value must be an integer')

        if value < 30 or value > 100:
            raise ValidationError(name, 'value must be in the range 30-100')

    def _operating_mode_validation(self, value):
        self._mode_validation('operating-mode', value, self.OPERATING_MODES)

    def _fan_mode_validation(self, value):
        self._mode_validation('fan-mode', value, self.FAN_MODES)

    def _mode_validation(self, name, value, valid_values):
        valid = False
        try:
            valid = value in valid_values
        except TypeError:
            pass
        if not valid:
            raise ValidationError(
                name,
                '{} is not a valid option. Options are {}'.format(
                    value, valid_values
                )
            )
