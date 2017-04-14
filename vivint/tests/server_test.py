import json
import pytest

from vivint.server import Server
from vivint.service import Service


def test_get_thermostats():
    app = Server(Service).app

    # Test happy path
    url = '/thermostats/'
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

    # Test redirect
    url = '/thermostats'
    response = app.request(url)
    assert '301 Moved Permanently' == response.status
    assert response.headers['Location'] == 'http://0.0.0.0:8080/thermostats/'


def test_get_thermostat():
    app = Server(Service).app

    # Test happy path
    url = '/thermostats/100/'
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

    # Test redirect
    url = '/thermostats/100'
    response = app.request(url)
    assert '301 Moved Permanently' == response.status
    assert response.headers['Location'] == 'http://0.0.0.0:8080/thermostats/100/'

    # Test errors
    for url in ['/thermostats/102/', '/thermostats/fake/']:
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
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data=payload, headers=headers)
    assert '200 OK' == response.status
    assert expected == json.loads(response.data)

    headers = {'Content-Type': 'application/json'}
    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data=payload, headers=headers)
    assert '200 OK' == response.status
    assert expected == json.loads(response.data)

    # Test redirect
    url = '/thermostats/100'
    response = app.request(url)
    assert '301 Moved Permanently' == response.status
    assert response.headers['Location'] == 'http://0.0.0.0:8080/thermostats/100/'

    # Test errors
    url = '/thermostats/102/'
    response = app.request(url, method='PATCH', data=payload, headers=headers)
    assert '404 Not Found' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '404 Not Found' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data='test', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data='[]', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data='100', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data='"test"', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PATCH', data=payload)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = app.request(url, method='PATCH', data=payload, headers=headers)
    assert '415 Unsupported Media Type' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '415 Unsupported Media Type' == response.data


def test_get_attribute():
    app = Server(Service).app

    # Test happy path
    url = '/thermostats/100/fan-mode/'
    response = app.request(url)
    assert '200 OK' == response.status
    assert response.headers['Content-Type'] == 'application/json'
    assert '{"result": "auto"}' == response.data

    # Test redirect
    url = '/thermostats/100/fan-mode'
    response = app.request(url)
    assert '301 Moved Permanently' == response.status
    assert response.headers['Location'] == 'http://0.0.0.0:8080/thermostats/100/fan-mode/'

    # Test errors
    for url in ['/thermostats/102/fan-mode/', '/thermostats/100/fake/']:
        response = app.request(url)
        assert '404 Not Found' == response.status
        assert response.headers['Content-Type'] == 'text/html'
        assert '404 Not Found' == response.data


def test_put_attribute():
    app = Server(Service).app

    # Test happy path
    url = '/thermostats/100/fan-mode/'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    response = app.request(url, method='PUT', data='"on"', headers=headers)
    assert '204 No Content' == response.status
    assert '204 No Content' == response.data

    url = '/thermostats/100/fan-mode/'
    headers = {'Content-Type': 'application/json'}
    response = app.request(url, method='PUT', data='"on"', headers=headers)
    assert '204 No Content' == response.status
    assert '204 No Content' == response.data

    # Test redirect
    url = '/thermostats/100/fan-mode'
    response = app.request(url, headers=headers)
    assert '301 Moved Permanently' == response.status
    assert response.headers['Location'] == 'http://0.0.0.0:8080/thermostats/100/fan-mode/'

    # Test errors
    url = '/thermostats/102/fan-mode/'
    response = app.request(url, method='PUT', data='"on"', headers=headers)
    assert '404 Not Found' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '404 Not Found' == response.data

    url = '/thermostats/100/current-temp/'
    response = app.request(url, method='PUT', data='80', headers=headers)
    assert '403 Forbidden' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '403 Forbidden' == response.data

    url = '/thermostats/100/cool-setpoint/'
    response = app.request(url, method='PUT', data='101', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/name/'
    response = app.request(url, method='PUT', data='testing', headers=headers)
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/'
    response = app.request(url, method='PUT', data='"on"')
    assert '400 Bad Request' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '400 Bad Request' == response.data

    url = '/thermostats/100/fan-mode/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = app.request(url, method='PUT', data='"on"', headers=headers)
    assert '415 Unsupported Media Type' == response.status
    assert response.headers['Content-Type'] == 'text/html'
    assert '415 Unsupported Media Type' == response.data
