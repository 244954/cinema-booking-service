from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Bookings


class BookingsDataInstanceObject(ABC):
    booking_id = 'booking_id'
    client_id = 'client_id'
    email = 'email'
    payment_id = 'payment_id'

    @abstractmethod
    def get_booking(self, booking_id):
        pass

    @abstractmethod
    def insert_booking(self, client_id, email, payment_id, commit: bool) -> int:
        pass

    @abstractmethod
    def delete_booking(self, booking_id):
        pass

    @abstractmethod
    def confirm_payment(self, booking_id):
        pass

    @abstractmethod
    def commit(self):
        pass


class BookingsDataInstanceObjectSQLAlchemy(BookingsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_booking(self, booking_id):
        booking = Bookings(booking_id=booking_id).first()
        return {
            BookingsDataInstanceObject.booking_id: booking.booking_id,
            BookingsDataInstanceObject.client_id: booking.client_id,
            BookingsDataInstanceObject.email: booking.email,
            BookingsDataInstanceObject.payment_id: booking.payment_id
        }

    def insert_booking(self, client_id, email, payment_id, commit=False):
        booking = Bookings(client_id=client_id, email=email, payment_id=payment_id)
        self.db.session.add(booking)
        if commit:
            self.commit()
            return booking.booking_id

    def delete_booking(self, booking_id):
        Bookings.query.filter_by(booking_id=booking_id).delete()

    def confirm_payment(self, booking_id):
        Tick

    def commit(self):
        self.db.session.commit()
