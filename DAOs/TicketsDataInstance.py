from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from utils.Others import offered_tickets
from models.Models import Tickets, Tickets_For_Showings, Seats, Halls, Showings
from DAOs.HallDataInstance import HallsDataInstanceObject as HaDIO
from DAOs.SeatsDataInstance import SeatsDataInstanceObject as SeDIO
from utils.AlchemyEncoder import AlchemyEncoder


class NotFoundInDBException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


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

    @abstractmethod
    def get_movie_id_for_ticket(self, ticket_id):
        pass

    @abstractmethod
    def get_tickets_for_booking(self, booking_id):
        pass

    @abstractmethod
    def insert_tickets_no_price(self, seat_ids: list, booking_id, showing_id, client_id) -> list:
        pass

    @abstractmethod
    def update_tickets(self, tickets):
        pass

    @abstractmethod
    def commit(self):
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

    def get_movie_id_for_ticket(self, ticket_id):
        showing = Showings.query.join(Tickets_For_Showings).join(Tickets).filter_by(ticket_id=ticket_id).with_entities(
            Showings.movie_id.label('movie_id')
        ).first()

        if showing:
            return showing.movie_id
        else:
            return None

    def get_tickets_for_booking(self, booking_id):
        tickets = Tickets.query.filter_by(booking_id=booking_id).join(Seats).join(Halls).with_entities(
            Seats.seat_number.label('seat_number'),
            Seats.row_number.label('row_number'),
            Halls.hall_name.label('hall_name'),
            Tickets.price.label('price'),
            Tickets.ticket_id.label('ticket_id')
        ).all()

        tickets_array = []
        for ticket in tickets:
            tickets_array.append(
                {
                    SeDIO.seat_number: ticket.seat_number,
                    SeDIO.row_number: ticket.row_number,
                    HaDIO.hall_name: ticket.hall_name,
                    TicketsDataInstanceObject.price: ticket.price,
                    TicketsDataInstanceObject.ticket_id: ticket.ticket_id
                }
            )
        if tickets_array:
            return tickets_array
        else:
            return None

    def insert_tickets_no_price(self, seats_found: list, booking_id, showing_id, client_id):
        for seat in seats_found:
            seat_id = seat[TicketsDataInstanceObject.seat_id]
            ticket = Tickets(seat_id=seat_id, booking_id=booking_id, price=0,
                             purchase_date=None, booking_date=func.now(), client_id=client_id)
            self.db.session.add(ticket)
            self.commit()                   # unfortunate, maybe make some workaround later
            ticket_id = ticket.ticket_id    # i need that id though
            ticket_showing = Tickets_For_Showings(showing_id=showing_id, ticket_id=ticket_id)
            self.db.session.add(ticket_showing)
            self.commit()
            seat[TicketsDataInstanceObject.ticket_id] = ticket_id
        return seats_found  # ticket_ids added

    def update_tickets(self, tickets):
        for ticket in tickets:
            selected_ticket = Tickets.query.filter_by(ticket_id=ticket[TicketsDataInstanceObject.ticket_id]).first()
            if not selected_ticket:
                raise NotFoundInDBException("Ticket not found")
            price = offered_tickets[ticket['ticket_type']]
            selected_ticket.price = price
            ticket[TicketsDataInstanceObject.price] = price
        self.commit()
        return tickets

    def commit(self):
        self.db.session.commit()
