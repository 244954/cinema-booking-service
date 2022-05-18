from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from models.Models import Seats, Tickets, Tickets_For_Showings
from utils.AlchemyEncoder import AlchemyEncoder


class SeatsDataInstanceObject(ABC):
    seat_id = 'seat_id'
    hall_id = 'hall_id'
    row_number = 'row_number'
    seat_number = 'seat_number'

    @abstractmethod
    def get_seat(self, seat_id):
        pass

    @abstractmethod
    def get_seats_for_showing(self, showing_id, hall_id):
        pass

    @abstractmethod
    def insert_seat(self, seat_id, hall_id, row_number, seat_number):
        pass

    @abstractmethod
    def commit(self):
        pass


class SeatsDataInstanceObjectSQLAlchemy(SeatsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_seat(self, seat_id):
        found_seat = Seats.query.filter_by(seat_id=seat_id).first()
        if found_seat:
            return {
                SeatsDataInstanceObject.seat_id: found_seat.seat_id,
                SeatsDataInstanceObject.hall_id: found_seat.hall_id,
                SeatsDataInstanceObject.row_number: found_seat.row_number,
                SeatsDataInstanceObject.seat_number: found_seat.seat_number
            }
        else:
            return None

    def get_seats_for_showing(self, showing_id, hall_id):
        found_seats = Seats.query.outerjoin(Tickets).outerjoin(Tickets_For_Showings,
                                                               Tickets_For_Showings.showing_id == showing_id).with_entities(
            Seats.seat_id.label('seat_id'),
            Seats.hall_id.label('hall_id'),
            Seats.row_number.label('row_number'),
            Seats.seat_number.label('seat_number'),
            func.count(Tickets_For_Showings.ticket_id).label('tickets')
        ).group_by(Seats).filter(Seats.hall_id == hall_id).all()

        e = AlchemyEncoder()
        json_list = []
        for u in found_seats:
            data = e.parse_sqlalchemy_object(u)
            for t in data:
                json_list.append(t)
        return json_list

    def insert_seat(self, seat_id, hall_id, row_number, seat_number):
        seat = Seats(seat_id=seat_id, hall_id=hall_id, row_number=row_number, seat_number=seat_number)
        self.db.session.add(seat)

    def commit(self):
        self.db.session.commit()
