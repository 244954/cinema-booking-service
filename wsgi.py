from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS, cross_origin
from models.Models import db
from utils.Response_codes import *
from transactions.Offer import *
from transactions.Booking import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Spanko123@localhost/cinema-booking-service'  # don't get excited, not my actual password for anything else
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zvbrepbrzinmob:353756c35468cb6c43a142b686d2f9120dfcc88968d95aeeb7a0e33fbcb5c542@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/dddakce3tomshd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)


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
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/select_seats', methods=['POST'])
def select_seats():
    if request.method == 'POST':
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/payment_completed/<successful>', methods=['PUT'])
def select_seats(successful):
    if request.method == 'PUT':
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


if __name__ == '__main__':
    with app.app_context():
        #  db.drop_all()
        #  db.create_all()
        app.run(debug=True)
