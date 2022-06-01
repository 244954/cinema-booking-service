import json
import functools
from DAOs.DAOFactory import SQLAlchemyDAOFactory, DAOFactory
from flask_app.config import DB_TYPE
from models.Models import db
from transactions.Booking import cancel_booking, confirm_booking
from transactions.Offer import showings_post
from mqrabbit import channel_publisher


dao_factory: DAOFactory

if DB_TYPE == 'SQLAlchemy':
    dao_factory = SQLAlchemyDAOFactory(db)
else:
    raise NotImplementedError("Can't handle database type: {}".format(DB_TYPE))


def cancel_reservation(ch, method, properties, body: bytes):
    print('cancel_reservation')
    print(body)
    payment_id = body.decode("utf-8")
    cancel_booking(dao_factory, payment_id, channel_publisher)


def new_showing(ch, method, properties, body: bytes):
    print('new_showing')
    print(body)
    showings_post(dao_factory, post_request=None, byte_json=body)


def confirm_reservation(ch, method, properties, body: bytes):
    print('confirm_reservation')
    print(body)
    payment_id = body.decode("utf-8")
    confirm_booking(dao_factory, payment_id, channel_publisher)


def test(ch, method, properties, body: bytes):
    print('test')
    print(json.loads(body))
