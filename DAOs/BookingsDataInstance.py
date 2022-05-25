from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Bookings


class BookingsDataInstanceObject(ABC):
    booking_id = 'booking_id'
    client_id = 'client_id'

    @abstractmethod
    def insert_booking(self, client_id, email, payment_id, commit: bool) -> int:
        pass

    @abstractmethod
    def commit(self):
        pass


class BookingsDataInstanceObjectSQLAlchemy(BookingsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def insert_booking(self, client_id, email, payment_id, commit=False):
        booking = Bookings(client_id=client_id, email=email, payment_id=payment_id)
        self.db.session.add(booking)
        if commit:
            self.commit()
            return booking.booking_id

    def commit(self):
        self.db.session.commit()
