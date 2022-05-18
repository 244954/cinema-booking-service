from DAOs.DAOFactory import DAOFactory
from DAOs.ShowingsDataInstance import ShowingsDataInstanceObject as ShDIO
from DAOs.SeatsDataInstance import SeatsDataInstanceObject as SeDIO
from jsonschemas.json_validate import validate_request_json
from flask import request, Response, jsonify, make_response
from utils.Generators import generate_response
from utils.Response_codes import *
from utils.Others import offered_tickets
from jsonschema import ValidationError


def get_showings(dao_factory: DAOFactory, post_request: request, from_date, to_date, movie_id, movie_language,
                 dubbing_language, subtitles_language, lector_language, age_limit) -> Response:
    showing_db_instance = dao_factory.create_showings_object()

    from_date_name = ('from_date', from_date)
    to_date_name = ('to_date', to_date)
    movie_id_name = ('movie_id', movie_id)
    age_limit_name = ('age_limit', age_limit)
    mandatory_parameters = [from_date_name, to_date_name, movie_id_name, age_limit_name]
    for name in mandatory_parameters:
        if name[1] is None:
            return generate_response('Mandatory {} query parameter missing'.format(name[0]), Status_code_invalid_data)

    found_showings_list = showing_db_instance.get_showings(from_date, to_date, movie_id, movie_language,
                                                           dubbing_language, subtitles_language,
                                                           lector_language, age_limit)

    response_list = {"showings": found_showings_list}
    response = make_response(jsonify(response_list), Status_code_ok)
    return response


def get_showing_detail(dao_factory: DAOFactory, post_request: request, showing_id) -> Response:
    showing_db_instance = dao_factory.create_showings_object()
    seats_db_instance = dao_factory.create_seats_object()

    found_showing = showing_db_instance.get_showing(showing_id)
    if found_showing is None:
        generate_response('Showing with id {} not found'.format(showing_id), Status_code_not_found)

    found_seats = seats_db_instance.get_seats_for_showing(found_showing[ShDIO.showing_id], found_showing[ShDIO.hall_id])

    response_list = {"seats": found_seats} | found_showing
    response = make_response(jsonify(response_list), Status_code_ok)
    return response


def select_seats_post(dao_factory: DAOFactory, post_request: request) -> Response:
    try:
        incoming_json = validate_request_json(post_request, 'jsonschemas/selected_seats_schema.json')
    except ValidationError as err:
        return generate_response(err.message, Status_code_bad_request)

    selected_seats = incoming_json['seats']
    hall_id = selected_seats['hall_id']
    client_id = selected_seats['client_id']
    showing_id = selected_seats['showing_id']
    selected_seats = selected_seats['selected_seats']
    seats_db_instance = dao_factory.create_seats_object()
    tickets_db_instance = dao_factory.create_tickets_object()
    bookings_db_instance = dao_factory.create_bookings_object()

    seats_found = []
    for seat in selected_seats:
        found_seat = seats_db_instance.get_seat(seat)
        if not found_seat:
            return generate_response('Selected seat not found', Status_code_bad_request)
        found_ticket = tickets_db_instance.get_ticket_for_seat_and_showing(found_seat[SeDIO.seat_id], showing_id)
        if found_ticket:
            return generate_response('Selected seat already taken', Status_code_bad_request)
        found_seat["available_tickets"] = offered_tickets
        seats_found.append(found_seat)

    booking_id = bookings_db_instance.insert_booking(client_id, commit=True)

    response_list = {"booking_id": booking_id, "seats": seats_found}
    response = make_response(jsonify(response_list), Status_code_ok)
    return response
