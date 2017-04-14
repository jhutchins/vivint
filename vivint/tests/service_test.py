import pytest

from vivint.errors import *
from vivint.service import Service


def test_name_validation():
    service = Service()
    name = 'name'

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, None)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, '')

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, True)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 75)

    service.set_attribute(100, name, 'Testing')
    assert 'Testing' == service.get_attribute(100, name)


def test_operating_mode_validation():
    mode_validation('operating-mode', Service.OPERATING_MODES)


def test_fan_mode_validation():
    mode_validation('fan-mode', Service.FAN_MODES)


def mode_validation(name, valid_values):
    service = Service()

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, None)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, True)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 75)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, {})

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, [])

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 'testing')

    for value in valid_values:
        service.set_attribute(100, name, value)
        assert value == service.get_attribute(100, name)

        service.set_attribute(100, name, str(value))
        assert value == service.get_attribute(100, name)


def test_cool_setpoint_validation():
    setpoint_validation('cool-setpoint')


def test_heat_setpoint_validation():
    setpoint_validation('heat-setpoint')


def setpoint_validation(name):
    service = Service()

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, None)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, True)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 'testing')

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, {})

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, [])

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 29)

    with pytest.raises(ValidationError):
        service.set_attribute(100, name, 101)

    for value in range(30, 101):
        service.set_attribute(100, name, value)
        assert value == service.get_attribute(100, name)
