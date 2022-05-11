from models.Models import Tickets, Halls, Seats, Showings
from flask import request, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from utils.Generators import generate_response
from utils.Response_codes import *
import datetime
import json
from jsonschema import validate, ValidationError


def halls_post(db: SQLAlchemy, post_request: request) -> Response:
    try:
        incoming_json = post_request.get_json()
    except Exception as ex:
        return generate_response('Malformed JSON data', Status_code_bad_request)

    with open('jsonschemas/halls_post_schema.json') as validator_file:
        json_validator = json.load(validator_file)
        try:
            validate(incoming_json, schema=json_validator)
        except ValidationError as err:
            return generate_response(err.message, Status_code_bad_request)

    hall_id = 'hall_id'
    cinema_id = 'cinema_id'
    hall_name = 'hall_name'
    mandatory_parameters = [hall_id, cinema_id, hall_name]
    message_list = []

    halls_list = incoming_json['halls']

    for obj in halls_list:
        parameters = {}
        for name in mandatory_parameters:
            if name in obj:
                parameters[name] = obj[name]

        found_hall = Halls.query.filter_by(hall_id=parameters[hall_id]).first()
        if found_hall:
            message_list.append({'msg': 'Object already exists', 'id': parameters[hall_id]})
        else:
            hall = Halls(hall_id=parameters[hall_id], cinema_id=parameters[cinema_id], hall_name=parameters[hall_name])
            message_list.append({'msg': 'Object created', 'id': parameters[hall_id]})
            db.session.add(hall)

    db.session.commit()
    response = generate_response(message_list, Status_code_created)
    return response


def seats_post(db: SQLAlchemy, post_request: request) -> Response:
    try:
        incoming_json = post_request.get_json()
    except Exception as ex:
        return generate_response('Malformed JSON data', Status_code_bad_request)

    with open('jsonschemas/seats_post_schema.json') as validator_file:
        json_validator = json.load(validator_file)
        try:
            validate(incoming_json, schema=json_validator)
        except ValidationError as err:
            return generate_response(err.message, Status_code_bad_request)

    seat_id = 'seat_id'
    hall_id = 'hall_id'
    row_number = 'row_number'
    seat_number = 'seat_number'
    mandatory_parameters = [seat_id, hall_id, row_number, seat_number]
    message_list = []

    seats_list = incoming_json['seats']

    for obj in seats_list:
        parameters = {}
        for name in mandatory_parameters:
            if name in obj:
                parameters[name] = obj[name]

        found_seat = Seats.query.filter_by(seat_id=parameters[seat_id]).first()
        if found_seat:
            message_list.append({'msg': 'Object already exists', 'id': parameters[seat_id]})
        else:
            seat = Seats(seat_id=parameters[seat_id], hall_id=parameters[hall_id], row_number=parameters[row_number], seat_number=parameters[seat_number])
            message_list.append({'msg': 'Object created', 'id': parameters[seat_id]})
            db.session.add(seat)

    db.session.commit()
    response = generate_response(message_list, Status_code_created)
    return response


def showings_post(db: SQLAlchemy, post_request: request) -> Response:
    try:
        incoming_json = post_request.get_json()
    except Exception as ex:
        return generate_response('Malformed JSON data', Status_code_bad_request)

    with open('jsonschemas/schowings_post_schema.json') as validator_file:
        json_validator = json.load(validator_file)
        try:
            validate(incoming_json, schema=json_validator)
        except ValidationError as err:
            return generate_response(err.message, Status_code_bad_request)

    showing_id = 'showing_id'
    showing_date = 'showing_date'
    hall_id = 'hall_id'
    movie_id = 'movie_id'
    movie_language = 'movie_language'
    age_limit = 'age_limit'

    subtitles = 'subtitles'
    dubbing = 'dubbing'
    lector = 'lector'
    subtitles_language = 'subtitles_language'
    lector_language = 'lector_language'
    dubbing_language = 'dubbing_language'

    mandatory_parameters = [showing_id, showing_date, hall_id, movie_id, movie_language, age_limit]
    optional_parameters = [subtitles, dubbing, lector, subtitles_language, lector_language, dubbing_language]
    message_list = []

    showings_list = incoming_json['showings']

    for obj in showings_list:
        parameters = {}
        for name in mandatory_parameters:
            if name in obj:
                parameters[name] = obj[name]
        for name in optional_parameters:
            if name in obj:
                parameters[name] = obj[name]
            else:
                parameters[name] = None

        found_showing = Showings.query.filter_by(showing_id=parameters[showing_id]).first()
        if found_showing:
            message_list.append({'msg': 'Object already exists', 'id': parameters[showing_id]})
        else:
            showing = Showings(showing_id=parameters[showing_id], showing_date=datetime.datetime.fromtimestamp(parameters[showing_date]),
                               hall_id=parameters[hall_id], movie_id=parameters[movie_id],
                               subtitles=parameters[subtitles], dubbing=parameters[dubbing], lector=parameters[lector],
                               movie_language=parameters[movie_language], subtitles_language=parameters[subtitles_language],
                               lector_language=parameters[lector_language], dubbing_language=parameters[dubbing_language],
                               age_limit=parameters[age_limit])
            message_list.append({'msg': 'Object created', 'id': parameters[showing_id]})
            db.session.add(showing)

    db.session.commit()
    response = generate_response(message_list, Status_code_created)
    return response


