class Service:

    FAN_MODES = {"auto", "on"},
    OPERATING_MODES = {"cool", "heat", "off"}

    def __init__(self):
        self._data = {
            100: {
                "id": 100,
                "name": "Upstairs Thermostat",
                "current-temp": 71,
                "operating-mode": "heat",
                "cool-setpoint": 75,
                "heat-setpoint": 65,
                "fan-mode": "auto"
            },
            101: {
                "id": 101,
                "name": "Downstairs Thermostat",
                "current-temp": 69,
                "operating-mode": "heat",
                "cool-setpoint": 75,
                "heat-setpoint": 65,
                "fan-mode": "auto"
            }
        }

    def thermostats(self):
        return self._data.values()

    def thermostat(self, id):
        try:
            id = int(id)
        except ValueError:
            return None

        return self._data.get(id)

    def get_attribute(self, id, name):
        thermostat = self.thermostat(id)
        if thermostat is None:
            return None

        return thermostat.get(name)

    def set_attribute(self, id, name, value):
        thermostat = self.thermostat(id)
        if thermostat is None or name not in thermostat:
            return None

        if not value:
            return False
        # TODO add more validation here
        thermostat[name] = value
        return True
