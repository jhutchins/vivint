import json
import pytest

from vivint.server import Server
from vivint.service import Service


def test_get_thermostats():
    app = Server(Service).app
    for url in ['/thermostats', '/thermostats/']:
        response = app.request(url)
        expected = json.dumps({'result': [
            {
                'name': 'Upstairs Thermostat',
                'operating-mode': 'heat',
                'cool-setpoint': 75,
                'heat-setpoint': 65,
                'fan-mode': 'auto',
                'current-temp': 71,
                'id': 100
            },
            {
                'name': 'Downstairs Thermostat',
                'operating-mode': 'heat',
                'cool-setpoint': 75,
                'heat-setpoint': 65,
                'fan-mode': 'auto',
                'current-temp': 69,
                'id': 101
            }
        ]})
        assert '200 OK' == response.status
        assert response.headers['Content-Type'] == 'application/json'
        assert expected == response.data


def test_get_thermostat():
    app = Server(Service).app

    # Test happy path
    for url in ['/thermostats/100', '/thermostats/100/']:
        response = app.request(url)
        expected = json.dumps({'result': {
            'name': 'Upstairs Thermostat',
            'operating-mode': 'heat',
            'cool-setpoint': 75,
            'heat-setpoint': 65,
            'fan-mode': 'auto',
            'current-temp': 71,
            'id': 100
        }})
        assert '200 OK' == response.status
        assert response.headers['Content-Type'] == 'application/json'
        assert expected == response.data

    # Test errors
    for url in ['/thermostats/102', '/thermostats/fake/']:
        response = app.request(url)
        assert '404 Not Found' == response.status
        assert response.headers['Content-Type'] == 'text/html'
        assert '404 Not Found' == response.data


def test_patch_thermostat():
    app = Server(Service).app

    # Test happy path
    payload = json.dumps({
        'name': 'New Name',
        'id': 5,
        'cool-setpoint': 'warm',
        'location': 'bathroom'
    })
    expected = {'result': {
        'name': 'ok',
        'id': 'value is readonly',
        'cool-setpoint': 'value must be an integer',
        'location': 'unknown attribute'
    }}
    for url in ['/thermostats/100', '/thermostats/100/']:
        response = app.request(url, method='PATCH', data=payload)
        assert '200 OK' == response.status
        # TODO this should have no content
        assert expected == json.loads(response.data)

    # Test errors
    url = '/thermostats/102'
    response = app.request(url, method='PATCH', data=payload)
    assert '404 Not Found' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '404 Not Found' == response.data

    # Test errors
    url = '/thermostats/100'
    response = app.request(url, method='PATCH', data='testing')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    # Test errors
    url = '/thermostats/100'
    response = app.request(url, method='PATCH', data='[]')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    # Test errors
    url = '/thermostats/100'
    response = app.request(url, method='PATCH', data='100')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    # Test errors
    url = '/thermostats/100'
    response = app.request(url, method='PATCH', data='"testing"')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data


def test_get_attribute():
    app = Server(Service).app

    # Test happy path
    for url in ['/thermostats/100/fan-mode', '/thermostats/100/fan-mode/']:
        response = app.request(url)
        assert '200 OK' == response.status
        assert response.headers['Content-Type'] == 'application/json'
        assert '{"result": "auto"}' == response.data

    # Test errors
    for url in ['/thermostats/102/fan-mode', '/thermostats/100/fake/']:
        response = app.request(url)
        assert '404 Not Found' == response.status
        assert response.headers['Content-Type'] == 'text/html'
        assert '404 Not Found' == response.data


def test_put_attribute():
    app = Server(Service).app

    # Test happy path
    for url in ['/thermostats/100/fan-mode', '/thermostats/100/fan-mode/']:
        response = app.request(url, method='PUT', data='"on"')
        assert '204 No Content' == response.status
        # TODO this should have no content
        assert '204 No Content' == response.data

    # Test errors
    url = '/thermostats/102/fan-mode'
    response = app.request(url, method='PUT', data='"on"')
    assert '404 Not Found' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '404 Not Found' == response.data

    url = '/thermostats/100/current-temp'
    response = app.request(url, method='PUT', data='80')
    assert '403 Forbidden' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '403 Forbidden' == response.data

    url = '/thermostats/100/cool-setpoint'
    response = app.request(url, method='PUT', data='101')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/name'
    response = app.request(url, method='PUT', data='testing')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data
