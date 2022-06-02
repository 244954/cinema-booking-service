import json
import logging
import os
import pika
import requests as rq
from mqrabbit.config import *
from transactions.Booking import cancel_booking, confirm_booking
from transactions.Offer import showings_post
from DAOs.DAOFactory import SQLAlchemyDAOFactory, DAOFactory
from flask_app.config import DB_TYPE


class RabbitChannels:
    def __init__(self, db, env):
        self.db = db

        if env == 'dev':
            self.URI = 'http://127.0.0.1:5000/'
        else:
            self.URI = 'https://cinema-booking-service.herokuapp.com/'

        self.dao_factory: DAOFactory
        if DB_TYPE == 'SQLAlchemy':
            self.dao_factory = SQLAlchemyDAOFactory(db)
        else:
            raise NotImplementedError("Can't handle database type: {}".format(DB_TYPE))

        logging.basicConfig()

        # Parse CLODUAMQP_URL (fallback to localhost)
        url = os.environ.get('CLOUDAMQP_URL', CLOUDAMQP_URL)
        params = pika.URLParameters(url + "?heartbeat=300")
        params.socket_timeout = SOCKET_TIMEOUT
        self.consumer_connection = pika.SelectConnection(parameters=params,
                                                         on_open_callback=self.on_open)
        self.producer_connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
        self.channel_publisher = self.producer_connection.channel()
        self.channel_publisher.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, durable=True)
        self.channel_publisher.queue_declare(queue=CHANNEL_REFUND_QUEUE, durable=True,
                                             arguments={"x-queue-type": "quorum"})
        self.channel_publisher.queue_declare(queue=CHANNEL_TICKET_NOTIFICATION_QUEUE, durable=True)
        self.channel_publisher.queue_declare(queue=CHANNEL_TEST_QUEUE, durable=True)

    def on_channel_open(self, channel):
        channel.basic_consume(CHANNEL_CANCEL_RESERVATION_QUEUE,
                              self.cancel_reservation,
                              auto_ack=AUTO_ACK)
        channel.basic_consume(CHANNEL_NEW_SHOWING_QUEUE,
                              self.new_showing,
                              auto_ack=AUTO_ACK)
        channel.basic_consume(CHANNEL_CONFIRM_RESERVATION_QUEUE,
                              self.confirm_reservation,
                              auto_ack=AUTO_ACK)
        channel.basic_consume(CHANNEL_TEST_QUEUE,
                              self.test,
                              auto_ack=AUTO_ACK)

    def on_open(self, connection_):
        connection_.channel(on_open_callback=self.on_channel_open)

    def start_mqrabbit(self):
        try:
            self.consumer_connection.ioloop.start()
        except KeyboardInterrupt:
            self.consumer_connection.close()
            self.consumer_connection.ioloop.start()

    def cancel_reservation(self, ch, method, properties, body: bytes):
        print('cancel_reservation')
        print(body)
        payment_id = body.decode("utf-8")
        uri = self.URI + 'bookings/cancel/' + payment_id
        r = rq.delete(uri)

    def new_showing(self, ch, method, properties, body: bytes):
        print('new_showing')
        print(body)
        showings_post(self.dao_factory, post_request=None, byte_json=body)

    def confirm_reservation(self, ch, method, properties, body: bytes):
        print('confirm_reservation')
        print(body)
        payment_id = body.decode("utf-8")
        uri = self.URI + 'bookings/confirm/' + payment_id
        print(uri)
        r = rq.put(uri)
        print(r.text)

    def test(self, ch, method, properties, body: bytes):
        print('test')
        print(json.loads(body))


"""

def on_channel_open(channel):
    channel.basic_consume(CHANNEL_CANCEL_RESERVATION_QUEUE,
                          cancel_reservation,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_NEW_SHOWING_QUEUE,
                          new_showing,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_CONFIRM_RESERVATION_QUEUE,
                          confirm_reservation,
                          auto_ack=AUTO_ACK)
    channel.basic_consume(CHANNEL_TEST_QUEUE,
                          test,
                          auto_ack=AUTO_ACK)


def on_open(connection_):
    connection_.channel(on_open_callback=on_channel_open)


def start_mqrabbit(mq_connection):
    try:
        mq_connection.ioloop.start()
    except KeyboardInterrupt:
        mq_connection.close()
        mq_connection.ioloop.start()


logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', CLOUDAMQP_URL)
params = pika.URLParameters(url+"?heartbeat=300")
params.socket_timeout = SOCKET_TIMEOUT
connection = pika.SelectConnection(parameters=params,
                                   on_open_callback=on_open)
connection2 = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel_publisher = connection2.channel()
channel_publisher.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_NOTIFICATION_QUEUE, durable=True)
channel_publisher.queue_declare(queue=CHANNEL_REFUND_QUEUE, durable=True, arguments={"x-queue-type": "quorum"})
channel_publisher.queue_declare(queue=CHANNEL_TICKET_NOTIFICATION_QUEUE, durable=True)
channel_publisher.queue_declare(queue=CHANNEL_TEST_QUEUE, durable=True)
#  how to publish message to MQRabbit customer
#  channel.basic_publish(exchange='', routing_key='cancel-reservation', body='User information')
from mqrabbit.callbacks import *

"""
