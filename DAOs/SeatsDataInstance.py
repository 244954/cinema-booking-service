from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Seats


class SeatsDataInstanceObject(ABC):
    seat_id = 'seat_id'
    hall_id = 'hall_id'
    row_number = 'row_number'
    seat_number = 'seat_number'

    @abstractmethod
    def get_seat(self, seat_id):
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

    def insert_seat(self, seat_id, hall_id, row_number, seat_number):
        seat = Seats(seat_id=seat_id, hall_id=hall_id, row_number=row_number, seat_number=seat_number)
        self.db.session.add(seat)

    def commit(self):
        self.db.session.commit()
