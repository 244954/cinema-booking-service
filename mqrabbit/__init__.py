import logging
import os
import pika
from mqrabbit.config import *
from mqrabbit.callbacks import *

logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', CLOUDAMQP_URL)
params = pika.URLParameters(url)
params.socket_timeout = SOCKET_TIMEOUT

connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel_cancel_reservation_send = connection.channel()  # start a channel
channel_cancel_reservation_send.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_QUEUE, durable=True)  # Declare a queue

#  how to publish message to MQRabbit customer
#  channel.basic_publish(exchange='', routing_key='cancel-reservation', body='User information')

channel_cancel_reservation_receive = connection.channel()  # start a channel
channel_cancel_reservation_receive.queue_declare(queue=CHANNEL_CANCEL_RESERVATION_QUEUE, durable=True)  # Declare a queue

# set up subscription on the queue
channel_cancel_reservation_receive.basic_consume(CHANNEL_CANCEL_RESERVATION_QUEUE,
                                                 cancel_reservation,
                                                 auto_ack=True)