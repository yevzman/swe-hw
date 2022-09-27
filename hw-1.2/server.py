from flask import Flask, jsonify
from flask import make_response, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
DB = dict()


def bad_request_response():
    response = app.response_class(
        response="Bad Request!\n",
        status=400
    )
    return response


def unsupported_media_type_response():
    response = app.response_class(
        response="Unsupported Media Type!\n",
        status=415
    )
    return response


def ok_response():
    response = app.response_class(
        response="Ok. Success!\n",
        status=200
    )
    return response


def not_found_response():
    response = app.response_class(
        response="Not Found!\n",
        status=404
    )
    return response


@app.route('/hello', methods=['GET'])
def hello_handler():
    response = app.response_class(
        response="HSE One Love!\n",
        status=200,
        mimetype='text/plain'
    )
    return response


@app.route('/set', methods=['POST'])
def set_value_handler():
    if request.mimetype != 'application/json':
        return unsupported_media_type_response()
    if 'key' not in request.json or 'value' not in request.json:
        return bad_request_response()
    DB[request.json['key']] = request.json['value']
    return ok_response()


@app.route('/get/<string:key>', methods=['GET'])
def get_value_handler(key):
    if key not in DB:
        return not_found_response()
    return jsonify(dict({"key": key, "value": DB[key]})), 200


@app.route('/divide', methods=['POST'])
def divide_handler():
    if request.mimetype != 'application/json':
        return unsupported_media_type_response()
    try:
        ans = str(int(request.json['dividend']) / int(request.json['divider']))
    except Exception:
        return bad_request_response()
    response = app.response_class(
        response=ans,
        mimetype='text/plain',
        status=200
    )
    return response


@app.errorhandler(HTTPException)
def error_handler(error):
    response = app.response_class(
        response="Method Not Allowed!\n",
        status=405
    )
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
