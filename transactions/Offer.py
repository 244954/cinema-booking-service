from models.Models import Tickets, Halls
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
