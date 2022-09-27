import server
import requests
import webbrowser
import json
import threading


def check_hello_handler():
    response = requests.get('http://localhost:8080/hello')

    assert response.text == 'HSE One Love!\n'
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'


def check_set_handler():
    url = 'http://localhost:8080/set'
    pair1 = {
        'key': 'name',
        'value': 'Yan'
    }
    pair2 = {
        'key': 'HSE'
        # no value
    }
    good_header = {'Content-Type': 'application/json'}
    bad_header = {'Content-Type': 'text/plain; charset=utf-8'}

    response = requests.post(url=url, headers=good_header, json=pair1)
    assert response.text == 'Ok. Success!\n'
    assert response.status_code == 200

    response = requests.post(url=url, headers=bad_header, json=pair1)
    assert response.text == 'Unsupported Media Type!\n'
    assert response.status_code == 415

    response = requests.post(url=url, headers=good_header, json=pair2)
    assert response.text == 'Bad Request!\n'
    assert response.status_code == 400


def check_get_handler():
    url = 'http://localhost:8080/get/'
    key1 = 'name'
    value1 = 'Yan'
    key2 = 'undefined'
    # no value2
    response = requests.get(url=url+key1)
    assert response.headers['Content-Type'] == 'application/json'
    json_res = json.loads(response.text)
    assert json_res['key'] == key1
    assert json_res['value'] == value1
    assert response.status_code == 200

    response = requests.get(url=url+key2)
    assert response.text == 'Not Found!\n'
    assert response.status_code == 404


def check_divide_handler():
    url = 'http://localhost:8080/divide'
    pair1 = {
        'dividend': 10,
        'divider': 2
    }
    pair2 = {
        'dividend': 3
        # no value
    }
    pair3 = {
        'dividend': 3,
        'divider': 0
    }
    good_header = {'Content-Type': 'application/json'}
    bad_header = {'Content-Type': 'text/plain; charset=utf-8'}

    response = requests.post(url=url, headers=good_header, json=pair1)
    assert float(response.text) == 5.0  # 10 / 2 = 5
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

    response = requests.post(url=url, headers=bad_header, json=pair1)
    assert response.text == 'Unsupported Media Type!\n'
    assert response.status_code == 415

    response1 = requests.post(url=url, headers=good_header, json=pair2)

    assert response1.text == 'Bad Request!\n'
    assert response1.status_code == 400

    response2 = requests.post(url=url, headers=good_header, json=pair3)
    assert response2.text == 'Bad Request!\n'
    assert response2.status_code == 400


if __name__ == '__main__':
    server_thread = threading.Thread(target=server.app.run, args=('localhost', 8080))
    server_thread.daemon = True
    server_thread.start()

    check_hello_handler()
    check_set_handler()
    check_get_handler()
    check_divide_handler()

    print('=================================================')
    print('All tests passed!')
    print('=================================================')
