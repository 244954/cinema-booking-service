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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Spanko123@localhost/cinema-booking-service'
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
        return Response(status=Status_code_not_found)


@app.route('/offer/halls', methods=['POST'])
def offer_halls():
    if request.method == 'POST':
        return halls_post(db, request)
    else:
        return Response(status=Status_code_not_found)


@app.route('/offer/seats', methods=['POST'])
def offer_seats():
    if request.method == 'POST':
        return seats_post(db, request)
    else:
        return Response(status=Status_code_not_found)


if __name__ == '__main__':
    with app.app_context():
        #  db.drop_all()
        #  db.create_all()
        app.run(debug=True)
