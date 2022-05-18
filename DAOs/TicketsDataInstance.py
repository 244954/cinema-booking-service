from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Tickets, Tickets_For_Showings


class TicketsDataInstanceObject(ABC):
    ticket_id = 'ticket_id'
    seat_id = 'seat_id'
    booking_id = 'booking_id'
    price = 'price'
    purchase_date = 'purchase_date'
    booking_date = 'booking_date'
    client_id = 'client_id'

    @abstractmethod
    def get_ticket_for_seat_and_showing(self, seat_id, showing_id):
        pass


class TicketsDataInstanceObjectSQLAlchemy(TicketsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_ticket_for_seat_and_showing(self, seat_id, showing_id):
        found_ticket = Tickets.query.join(Tickets_For_Showings).filter(Tickets.seat_id == seat_id,
                                                                       Tickets_For_Showings.showing_id == showing_id).first()
        if found_ticket:
            return {
                TicketsDataInstanceObject.ticket_id: found_ticket.ticket_id,
                TicketsDataInstanceObject.seat_id: found_ticket.seat_id,
                TicketsDataInstanceObject.booking_id: found_ticket.booking_id,
                TicketsDataInstanceObject.price: found_ticket.price,
                TicketsDataInstanceObject.purchase_date: found_ticket.purchase_date,
                TicketsDataInstanceObject.booking_date: found_ticket.booking_date,
                TicketsDataInstanceObject.client_id: found_ticket.client_id
            }
        else:
            return None
