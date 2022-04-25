from models.Models import Tickets, Halls, Seats
from flask import request, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from utils.Generators import generate_response
from utils.Response_codes import *


def halls_post(db: SQLAlchemy, post_request: request) -> Response:
    try:
        json = post_request.get_json()
    except Exception as ex:
        return generate_response('Malformed JSON data', Status_code_bad_request)

    if not json:
        return generate_response('Provided list is empty. No data provided', Status_code_nothing_found)

    hall_id = 'hall_id'
    cinema_id = 'cinema_id'
    hall_name = 'hall_name'
    mandatory_parameters = [hall_id, cinema_id, hall_name]
    message_list = []

    if 'halls' not in json:
        return generate_response('Provided list is empty. No data provided', Status_code_nothing_found)
    halls_list = json['halls']

    for obj in halls_list:
        parameters = {}
        for name in mandatory_parameters:
            if name in obj:
                parameters[name] = obj[name]
            else:
                db.session.rollback()
                db.session.close()
                return generate_response('Mandatory {} parameter missing'.format(name), Status_code_invalid_data)

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
        json = post_request.get_json()
    except Exception as ex:
        return generate_response('Malformed JSON data', Status_code_bad_request)

    if not json:
        return generate_response('Provided list is empty. No data provided', Status_code_nothing_found)

    seat_id = 'seat_id'
    hall_id = 'hall_id'
    row_number = 'row_number'
    seat_number = 'seat_number'
    mandatory_parameters = [seat_id, hall_id, row_number, seat_number]
    message_list = []

    if 'seats' not in json:
        return generate_response('Provided list is empty. No data provided', Status_code_nothing_found)
    seats_list = json['seats']

    for obj in seats_list:
        parameters = {}
        for name in mandatory_parameters:
            if name in obj:
                parameters[name] = obj[name]
            else:
                db.session.rollback()
                db.session.close()
                return generate_response('Mandatory {} parameter missing'.format(name), Status_code_invalid_data)

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
