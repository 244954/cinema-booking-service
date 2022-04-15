from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship

Base = declarative_base()
db = SQLAlchemy()


class Halls(db.Model):
    __tablename__ = 'Halls'
    hall_id = Column('hall_id', Integer, primary_key=True, nullable=False)
    cinema_id = Column('cinema_id', Integer, nullable=False)
    hall_name = Column('hall_name', Text, nullable=False)

    seats = relationship('Seats', backref='Seats.hall_id',
                         primaryjoin='Halls.hall_id==Seats.hall_id',
                         lazy='dynamic')

    def __init__(self, hall_id, cinema_id, hall_name):
        self.hall_id = hall_id
        self.cinema_id = cinema_id
        self.hall_name = hall_name


class Seats(db.Model):
    __tabname__ = 'Seats'
    seat_id = Column('seat_id', Integer, primary_key=True, nullable=False)
    hall_id = Column('hall_id', Integer, ForeignKey(Halls.hall_id), nullable=False)
    row_number = Column('row_number', Integer, nullable=False)
    seat_number = Column('seat_number', Integer, nullable=False)

    halls = relationship('Halls', foreign_keys='Seats.hall_id')


class Showings(db.Model):
    __tabname__ = 'Showings'
    showing_id = Column('showing_id', Integer, primary_key=True, nullable=False)
    showing_date = Column('showing_date', TIMESTAMP(timezone=False), nullable=False)
    hall_id = Column('hall_id', Integer, ForeignKey(Halls.hall_id), nullable=False)
    movie_id = Column('movie_id', Integer, nullable=False)
    subtitles = Column('subtitles', Boolean)
    dubbing = Column('dubbing', Boolean)
    lector = Column('lector', Boolean)
    movie_language = Column('movie_language', Text, nullable=False)
    subtitles_language = Column('subtitles_language', Text)
    lector_language = Column('lector_language', Text)
    dubbing_language = Column('dubbing_language', Text)
    age_limit = Column('age_limit', Integer, nullable=False)


class Client_Accounts(db.Model):
    __tabname__ = 'Client_Accounts'
    client_id = Column('client_id', Integer, primary_key=True, nullable=True)
    login = Column('login', Text, nullable=False)
    password = Column('password', Text, nullable=False)
    loyalty_points = Column('loyalty_points', Integer, default=0, nullable=False)
    birth_date = Column('birth_date', Date, nullable=False)
    email = Column('email', Text, nullable=False)
    phone_number = Column('phone_number', Text, nullable=True)


class Bookings(db.Model):
    __tabname__ = 'Bookings'
    booking_id = Column('booking_id', Integer, nullable=False)
    client_id = Column('client_id', Integer, ForeignKey(Client_Accounts.client_id), nullable=False)


class Tickets(db.Model):
    __tabname__ = 'Tickets'
    ticket_id = Column('ticket_id', Integer, primary_key=True, nullable=False)
    seat_id = Column('seat_id', Integer, ForeignKey(Seats.seat_id), nullable=False)
    booking_id = Column('booking_id', Integer, ForeignKey(Bookings.booking_id), nullable=False)
    price = Column('price', Numeric, nullable=False)
    purchase_date = Column('purchase_date', TIMESTAMP(timezone=True), nullable=False)
    booking_date = Column('booking_date', TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
    client_id = Column('client_id', Integer, ForeignKey(Client_Accounts.client_id), nullable=True)  # ?


class Tickets_For_Showings(db.Model):
    __tabname__ = 'Tickets_For_Showings'
    showing_id = Column('showing_id', Integer, ForeignKey(Showings.showing_id), nullable=False)
    ticket_id = Column('ticket_id', Integer, ForeignKey(Tickets.ticket_id), nullable=False)

