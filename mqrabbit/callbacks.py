import json

from DAOs.DAOFactory import SQLAlchemyDAOFactory, DAOFactory
from flask_app.config import DB_TYPE
from models.Models import db


dao_factory: DAOFactory

if DB_TYPE == 'SQLAlchemy':
    dao_factory = SQLAlchemyDAOFactory(db)
else:
    raise NotImplementedError("Can't handle database type: {}".format(DB_TYPE))


def cancel_reservation(ch, method, properties, body):
    print(body)


def new_showing(ch, method, properties, body):
    print(body)


def confirm_reservation(ch, method, properties, body):
    print(body)


def test(ch, method, properties, body):
    print(json.loads(body))
