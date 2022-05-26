from pika.channel import Channel
from mqrabbit.config import CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, CHANNEL_TEST_QUEUE, \
    CHANNEL_TICKET_NOTIFICATION_QUEUE, CHANNEL_REFUND_QUEUE
from DAOs.DAOFactory import DAOFactory
from DAOs.ShowingsDataInstance import ShowingsDataInstanceObject as ShDIO
from DAOs.SeatsDataInstance import SeatsDataInstanceObject as SeDIO
from DAOs.TicketsDataInstance import NotFoundInDBException, TicketsDataInstanceObject as TiDIO
from DAOs.BookingsDataInstance import BookingsDataInstanceObject as BoDIO
from jsonschemas.json_validate import validate_request_json, validate_bytes_json
from flask import request, Response, jsonify, make_response
from utils.Generators import generate_response
from utils.Response_codes import *
from utils.Others import offered_tickets, JSONEncoder
from jsonschema import ValidationError
import json


def test_post(dao_factory: DAOFactory, post_request: request, channel: Channel) -> Response:
    json_msg = {"hello": "world"}
    channel.basic_publish(exchange='', routing_key=CHANNEL_TEST_QUEUE, body=json.dumps(json_msg))
    response = generate_response('Ok', Status_code_ok)
    return response


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
        return generate_response('Showing with id {} not found'.format(showing_id), Status_code_not_found)

    found_seats = seats_db_instance.get_seats_for_showing(found_showing[ShDIO.showing_id], found_showing[ShDIO.hall_id])

    response_list = {"seats": found_seats} | found_showing
    response = make_response(jsonify(response_list), Status_code_ok)
    return response


def select_seats_post(dao_factory: DAOFactory, post_request: request, channel: Channel) -> Response:
    try:
        incoming_json = validate_request_json(post_request, 'jsonschemas/selected_seats_schema.json')
    except ValidationError as err:
        return generate_response(err.message, Status_code_bad_request)

    selected_seats = incoming_json['seats']
    hall_id = selected_seats['hall_id']
    client_id = selected_seats['client_id']
    email = selected_seats['email']
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

    booking_id = bookings_db_instance.insert_booking(client_id, email, None, commit=True)
    seats_found = tickets_db_instance.insert_tickets_no_price(seats_found, booking_id, showing_id, client_id)
    tickets = tickets_db_instance.get_tickets_for_booking(booking_id)
    #  if not paid for in 20 minutes delete tickets

    json_to_send = {
        "email": email,
        "tickets": tickets,
        "movie_name": None  # get it from somewhere
    }
    channel.basic_publish(exchange='', routing_key=CHANNEL_TICKET_NOTIFICATION_QUEUE, body=json.dumps(json_to_send, cls=JSONEncoder))

    response_list = {"booking_id": booking_id, "showing_id": showing_id, "seats": seats_found}
    response = make_response(jsonify(response_list), Status_code_ok)
    return response


def tickets_put(dao_factory: DAOFactory, post_request: request) -> Response:
    try:
        incoming_json = validate_request_json(post_request, 'jsonschemas/tickets_post_schema.json')
    except ValidationError as err:
        return generate_response(err.message, Status_code_bad_request)

    new_tickets = incoming_json['tickets']
    tickets_db_instance = dao_factory.create_tickets_object()

    try:
        tickets_db_instance.update_tickets(new_tickets)
    except NotFoundInDBException as err:
        return generate_response(err.message, Status_code_not_found)
    response = generate_response('Tickets successfully updated', Status_code_ok)
    return response


def cancel_booking(dao_factory: DAOFactory, json_bytes: bytes, channel: Channel):
    try:
        incoming_json = validate_bytes_json(bytes, 'jsonschemas/cancel_booking_schema.json')
    except ValidationError as err:
        print(err.message)
        return

    booking_id = incoming_json['booking_id']
    bookings_db_instance = dao_factory.create_bookings_object()
    tickets_db_instance = dao_factory.create_tickets_object()

    booking = bookings_db_instance.get_booking(booking_id)
    tickets = tickets_db_instance.get_tickets_for_booking(booking_id)
    json_to_send = {
        "email": booking[BoDIO.booking_id],
        "tickets": tickets,
        "movie_name": None  # get it from somewhere
    }

    bookings_db_instance.delete_booking(booking_id)  # cascade should take care of tickets too
    bookings_db_instance.commit()

    channel.basic_publish(exchange='', routing_key=CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, body=json.dumps(json_to_send, cls=JSONEncoder))
    return


def confirm_booking(dao_factory: DAOFactory, json_bytes: bytes, channel: Channel):
    try:
        incoming_json = validate_bytes_json(bytes, 'jsonschemas/confirm_booking_schema.json')
    except ValidationError as err:
        print(err.message)
        return

    booking_id = incoming_json['booking_id']
    payment_date = incoming_json['payment_date']
    bookings_db_instance = dao_factory.create_bookings_object()
    tickets_db_instance = dao_factory.create_tickets_object()

    bookings_db_instance.confirm_payment(booking_id, payment_date)
    bookings_db_instance.commit()
    booking = bookings_db_instance.get_booking(booking_id)
    tickets = tickets_db_instance.get_tickets_for_booking(booking_id)
    json_to_send = {
        "email": booking[BoDIO.booking_id],
        "tickets": tickets,
        "movie_name": None  # get it from somewhere
    }

    channel.basic_publish(exchange='', routing_key=CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, body=json.dumps(json_to_send, cls=JSONEncoder))
    return


def delete_booking_by_id(dao_factory: DAOFactory, json_bytes: bytes, channel: Channel, booking_id):
    booking_id = int(booking_id)
    bookings_db_instance = dao_factory.create_bookings_object()

    booking = bookings_db_instance.get_booking(booking_id)
    if booking is None:
        return generate_response('Booking with id {} not found'.format(booking_id), Status_code_not_found)
    bookings_db_instance.delete_booking(booking_id)  # cascade should take care of tickets too

    json_to_send = json.dumps(
        {
            "payment_id": booking[BoDIO.payment_id]
        },
        cls=JSONEncoder
    )
    channel.basic_publish(exchange='', routing_key=CHANNEL_REFUND_QUEUE, body=json_to_send)
    bookings_db_instance.commit()
    response = make_response("Booking deleted", Status_code_ok)
    return response


def get_bookings_from_email(dao_factory: DAOFactory, email):
    bookings_db_instance = dao_factory.create_bookings_object()
    bookings = bookings_db_instance.get_bookings(email)

    response_list = {"bookings": bookings}
    response = make_response(jsonify(response_list), Status_code_ok)
    return response
