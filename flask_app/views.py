from flask import request, Response
from flask_app import app, db
from transactions.Booking import get_showing_detail, get_showings, select_seats_post
from transactions.Offer import seats_post, halls_post, showings_post
from utils.Generators import generate_response
from utils.Response_codes import *


@app.route('/booking', methods=['POST'])
def booking():
    if request.method == 'POST':
        return Response(status=Status_code_ok)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/halls', methods=['POST'])
def offer_halls():
    if request.method == 'POST':
        return halls_post(db, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/seats', methods=['POST'])
def offer_seats():
    if request.method == 'POST':
        return seats_post(db, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/showings', methods=['POST'])
def offer_showings():
    if request.method == 'POST':
        return showings_post(db, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/showings/<movie_id>', methods=['GET'])
def showings(movie_id):
    if request.method == 'GET':  # here goes plenty of query parameters
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        movie_language = request.args.get('movie_language')
        dubbing_language = request.args.get('dubbing_language')
        subtitles_language = request.args.get('subtitles_language')
        lector_language = request.args.get('lector_language')
        age_limit = request.args.get('age_limit')
        return get_showings(db, request, from_date, to_date, movie_id, movie_language, dubbing_language,
                            subtitles_language, lector_language, age_limit)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/showings/detail/<showing_id>', methods=['GET'])
def showings_detail(showing_id):
    if request.method == 'GET':
        return get_showing_detail(db, request, showing_id)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/select_seats', methods=['POST'])
def select_seats():
    if request.method == 'POST':
        return select_seats_post(db, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/payment_completed/<successful>', methods=['PUT'])
def payment_completed(successful):
    if request.method == 'PUT':
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)
