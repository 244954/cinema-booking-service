from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Halls(db.Model):
    __tablename__ = 'Halls'
    hall_id = Column('hall_id', Integer, primary_key=True, nullable=False)
    cinema_id = Column('cinema_id', Integer, nullable=False)
    hall_name = Column('hall_name', Text, nullable=False)

    seats = relationship('Seats', backref='Seats.hall_id',
                         primaryjoin='Halls.hall_id==Seats.hall_id',
                         lazy='dynamic')
    showings = relationship('Showings', backref='Showings.hall_id',
                            primaryjoin='Halls.hall_id==Showings.hall_id',
                            lazy='dynamic')

    def __init__(self, hall_id, cinema_id, hall_name):
        self.hall_id = hall_id
        self.cinema_id = cinema_id
        self.hall_name = hall_name


class Seats(db.Model):
    __tablename__ = 'Seats'
    seat_id = Column('seat_id', Integer, primary_key=True, nullable=False)
    hall_id = Column('hall_id', Integer, ForeignKey(Halls.hall_id), nullable=False)
    row_number = Column('row_number', Integer, nullable=False)
    seat_number = Column('seat_number', Integer, nullable=False)

    halls = relationship('Halls', foreign_keys='Seats.hall_id')
    tickets = relationship('Tickets', backref='Tickets.seat_id',
                           primaryjoin='Seats.seat_id==Tickets.seat_id',
                           lazy='dynamic', cascade="all,delete")

    def __init__(self, seat_id, hall_id, row_number, seat_number):
        self.seat_id = seat_id
        self.hall_id = hall_id
        self.row_number = row_number
        self.seat_number = seat_number


class Showings(db.Model):
    __tablename__ = 'Showings'
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

    halls = relationship('Halls', foreign_keys='Showings.hall_id')
    ticket = relationship('Tickets_For_Showings', backref='Tickets_For_Showings.showing_id',
                          primaryjoin='Showings.showing_id==Tickets_For_Showings.showing_id',
                          lazy='dynamic', cascade="all,delete")

    def __init__(self, showing_id, showing_date, hall_id, movie_id, subtitles, dubbing, lector, movie_language,
                 subtitles_language, lector_language, dubbing_language, age_limit):
        self.showing_id = showing_id
        self.showing_date = showing_date
        self.hall_id = hall_id
        self.movie_id = movie_id
        self.subtitles = subtitles
        self.dubbing = dubbing
        self.lector = lector
        self.movie_language = movie_language
        self.subtitles_language = subtitles_language
        self.lector_language = lector_language
        self.dubbing_language = dubbing_language
        self.age_limit = age_limit


class Bookings(db.Model):
    __tablename__ = 'Bookings'
    booking_id = Column('booking_id', Integer, primary_key=True, nullable=False)
    client_id = Column('client_id', Integer, nullable=False)

    tickets = relationship('Tickets', backref='Tickets.booking_id',
                           primaryjoin='Bookings.booking_id==Tickets.booking_id',
                           lazy='dynamic', cascade="all,delete")


class Tickets(db.Model):
    __tablename__ = 'Tickets'
    ticket_id = Column('ticket_id', Integer, primary_key=True, nullable=False)
    seat_id = Column('seat_id', Integer, ForeignKey(Seats.seat_id), nullable=False)
    booking_id = Column('booking_id', Integer, ForeignKey(Bookings.booking_id), nullable=False)
    price = Column('price', Numeric, nullable=False)
    purchase_date = Column('purchase_date', TIMESTAMP(timezone=True), nullable=False)
    booking_date = Column('booking_date', TIMESTAMP(timezone=False), server_default=func.now(), nullable=False)
    client_id = Column('client_id', Integer, nullable=True)  # ?
    #  client_id = Column('client_id', Integer, ForeignKey(Client_Accounts.client_id), nullable=True)  # ?

    seats = relationship('Seats', foreign_keys='Tickets.seat_id')
    bookings = relationship(Bookings, foreign_keys='Tickets.booking_id')
    showing = relationship('Tickets_For_Showings', backref='Tickets_For_Showings.ticket_id',
                           primaryjoin='Tickets.ticket_id==Tickets_For_Showings.ticket_id',
                           lazy='dynamic', cascade="all,delete")

    def __init__(self, tickets_id, seat_id, booking_id, price, purchase_date, booking_date, client_id):
        self.ticket_id = tickets_id
        self.seat_id = seat_id
        self.booking_id = booking_id
        self.price = price
        self.purchase_date = purchase_date
        self.booking_date = booking_date
        self.client_id = client_id


class Tickets_For_Showings(db.Model):
    __tablename__ = 'Tickets_For_Showings'
    showing_id = Column('showing_id', Integer, ForeignKey(Showings.showing_id), primary_key=True, nullable=False)
    ticket_id = Column('ticket_id', Integer, ForeignKey(Tickets.ticket_id), primary_key=True, nullable=False)

    showing = relationship('Showings', foreign_keys='Tickets_For_Showings.showing_id')
    ticket = relationship('Tickets', foreign_keys='Tickets_For_Showings.ticket_id')

    def __init__(self, showing_id, ticket_id):
        self.showing_id = showing_id
        self.ticket_id = ticket_id
