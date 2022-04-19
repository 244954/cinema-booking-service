from flask import Response, make_response, jsonify


def generate_response(message, response_code: int) -> Response:
    response = make_response(jsonify({'messages': message}), response_code)
    return response
