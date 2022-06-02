from flask import request, Response
from pika.channel import Channel
from utils.Generators import generate_response
from utils.Response_codes import *
from jsonschema import ValidationError
from DAOs.DAOFactory import DAOFactory
from DAOs.HallDataInstance import HallsDataInstanceObject as HaDIO
from DAOs.SeatsDataInstance import SeatsDataInstanceObject as SeDIO
from DAOs.ShowingsDataInstance import ShowingsDataInstanceObject as ShDIO
from jsonschemas.json_validate import validate_request_json, validate_bytes_json
import datetime
import json


def halls_post(dao_factory: DAOFactory, post_request: request) -> Response:
    try:
        incoming_json = validate_request_json(post_request, 'jsonschemas/halls_post_schema.json')
    except ValidationError as err:
        return generate_response(err.message, Status_code_bad_request)

    halls_list = incoming_json['halls']
    hall_db_instance = dao_factory.create_halls_object()
    message_list = []

    for hall in halls_list:

        found_hall = hall_db_instance.get_hall(hall[HaDIO.hall_id])
        if found_hall:
            message_list.append({'msg': 'Object already exists', 'id': found_hall[HaDIO.hall_id]})
        else:
            hall_db_instance.insert_hall(hall[HaDIO.hall_id],
                                         hall[HaDIO.cinema_id],
                                         hall[HaDIO.hall_name])
            message_list.append({'msg': 'Object created', 'id': hall[HaDIO.hall_id]})

    hall_db_instance.commit()
    response = generate_response(message_list, Status_code_created)
    return response


def seats_post(dao_factory: DAOFactory, post_request: request) -> Response:
    try:
        incoming_json = validate_request_json(post_request, 'jsonschemas/seats_post_schema.json')
    except ValidationError as err:
        return generate_response(err.message, Status_code_bad_request)

    seats_list = incoming_json['seats']
    seats_db_instance = dao_factory.create_seats_object()
    message_list = []

    for seat in seats_list:
        found_seat = seats_db_instance.get_seat(seat[SeDIO.seat_id])
        if found_seat:
            message_list.append({'msg': 'Object already exists', 'id': found_seat[SeDIO.seat_id]})
        else:
            seats_db_instance.insert_seat(seat[SeDIO.seat_id],
                                          seat[SeDIO.hall_id],
                                          seat[SeDIO.row_number],
                                          seat[SeDIO.seat_number])
            message_list.append({'msg': 'Object created', 'id': seat[SeDIO.seat_id]})

    seats_db_instance.commit()
    response = generate_response(message_list, Status_code_created)
    return response


def showings_post(dao_factory: DAOFactory, post_request: request, multiple: bool) -> Response:
    try:
        if multiple:
            incoming_json = validate_request_json(post_request, 'jsonschemas/schowings_post_schema.json')
        else:
            incoming_json = validate_request_json(post_request, 'jsonschemas/schowing_post_from_offer_schema.json')
    except ValidationError as err:
        print(err.message)
        return generate_response(err.message, Status_code_bad_request)

    if 'showings' in incoming_json:
        showings_list = incoming_json['showings']
    else:
        showings_list = [incoming_json]
    showing_db_instance = dao_factory.create_showings_object()
    message_list = []

    for showing in showings_list:

        found_showing = showing_db_instance.get_showing(showing[ShDIO.showing_id])
        if found_showing:
            message_list.append({'msg': 'Object already exists', 'id': showing[ShDIO.showing_id]})
        else:
            if ShDIO.showing_date in showing:
                showing_date = showing[ShDIO.showing_date]
                if showing_date > 9999999999:  # milliseconds detector
                    showing_date = showing_date // 1000
                    formatted_date = datetime.datetime.fromtimestamp(showing_date)
                else:
                    formatted_date = datetime.datetime.fromtimestamp(showing_date)
            else:
                formatted_date = None
            showing_db_instance.insert_showing(
                showing_id=showing[ShDIO.showing_id] if ShDIO.showing_id in showing else None,
                showing_date=formatted_date,
                hall_id=showing[ShDIO.hall_id] if ShDIO.hall_id in showing else None,
                movie_id=showing[ShDIO.movie_id] if ShDIO.movie_id in showing else None,
                subtitles=showing[ShDIO.subtitles] if ShDIO.subtitles in showing else None,
                dubbing=showing[ShDIO.dubbing] if ShDIO.dubbing in showing else None,
                lector=showing[ShDIO.lector] if ShDIO.lector in showing else None,
                movie_language=showing[ShDIO.movie_language] if ShDIO.movie_language in showing else None,
                subtitles_language=showing[ShDIO.subtitles_language] if ShDIO.subtitles_language in showing else None,
                lector_language=showing[ShDIO.lector_language] if ShDIO.lector_language in showing else None,
                dubbing_language=showing[ShDIO.dubbing_language] if ShDIO.dubbing_language in showing else None,
                age_limit=showing[ShDIO.age_limit] if ShDIO.age_limit in showing else None,
            )
            message_list.append({'msg': 'Object created', 'id': showing[ShDIO.showing_id]})

    showing_db_instance.commit()
    response = generate_response(message_list, Status_code_created)
    return response
