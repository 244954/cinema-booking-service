import logging
import os
import pika
import py_eureka_client.eureka_client as eureka_client
from flask import Flask
from models.Models import db
from transactions.Booking import *
from transactions.Offer import *
from threading import Thread


def config_app(env, sqlalchemy_db):
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = 'secret!'

    if env == 'dev':
        new_app.debug = True
        new_app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Spanko123@localhost/cinema-booking-service'  # don't get excited, not my actual password for anything else
    else:
        new_app.debug = False
        new_app.config[
            'SQLALCHEMY_DATABASE_URI'] = 'postgres://zvbrepbrzinmob:353756c35468cb6c43a142b686d2f9120dfcc88968d95aeeb7a0e33fbcb5c542@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/dddakce3tomshd'

    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    new_app.config['CORS_HEADERS'] = 'Content-Type'
    sqlalchemy_db.init_app(new_app)

    return new_app


def config_eureka():
    eureka_client.init(eureka_server="https://eureka-server-cinema.herokuapp.com/eureka",
                       app_name="cinema-booking-service")


def config_mqrabbit():
    logging.basicConfig()

    # Parse CLODUAMQP_URL (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL',
                         'amqps://wkopublf:3ry2ohNtiaf2nYC-QTzFYO3MQioPMXja@bonobo.rmq.cloudamqp.com/wkopublf')
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
    channel_cancel_reservation_send = connection.channel()  # start a channel
    channel_cancel_reservation_send.queue_declare(queue='cancel-reservation', durable=True)  # Declare a queue

    #  how to publish message to MQRabbit customer
    #  channel.basic_publish(exchange='', routing_key='cancel-reservation', body='User information')

    channel_cancel_reservation_receive = connection.channel()  # start a channel
    channel_cancel_reservation_receive.queue_declare(queue='cancel-reservation', durable=True)  # Declare a queue

    # set up subscription on the queue
    channel_cancel_reservation_receive.basic_consume('cancel-reservation',
                                                     cancel_reservation,
                                                     auto_ack=True)
    return channel_cancel_reservation_send, channel_cancel_reservation_receive


def cancel_reservation(ch, method, properties, body):
    new_endpoint_for_cancelation(body)


app = config_app('prod', db)


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
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/payment_completed/<successful>', methods=['PUT'])
def payment_completed(successful):
    if request.method == 'PUT':
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


def new_endpoint_for_cancelation(body):
    print(body)


if __name__ == '__main__':
    config_eureka()
    channel1, channel2 = config_mqrabbit()
    with app.app_context():
        #  db.drop_all()
        #  db.create_all()
        thread = Thread(target=channel2.start_consuming)
        thread.start()
        app.run(debug=True)
