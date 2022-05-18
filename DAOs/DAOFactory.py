from DAOs.HallDataInstance import HallsDataInstanceObject, HallsDataInstanceObjectSQLAlchemy
from DAOs.SeatsDataInstance import SeatsDataInstanceObject, SeatsDataInstanceObjectSQLAlchemy
from DAOs.ShowingsDataInstance import ShowingsDataInstanceObject, ShowingsDataInstanceObjectSQLAlchemy
from DAOs.TicketsDataInstance import TicketsDataInstanceObject, TicketsDataInstanceObjectSQLAlchemy
from DAOs.BookingsDataInstance import BookingsDataInstanceObject, BookingsDataInstanceObjectSQLAlchemy
from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy


class DAOFactory(ABC):
    @abstractmethod
    def create_halls_object(self) -> HallsDataInstanceObject:
        pass

    @abstractmethod
    def create_seats_object(self) -> SeatsDataInstanceObject:
        pass

    @abstractmethod
    def create_showings_object(self) -> ShowingsDataInstanceObject:
        pass

    @abstractmethod
    def create_tickets_object(self) -> TicketsDataInstanceObject:
        pass

    @abstractmethod
    def create_bookings_object(self) -> BookingsDataInstanceObject:
        pass


class SQLAlchemyDAOFactory(DAOFactory):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_halls_object(self):
        return HallsDataInstanceObjectSQLAlchemy(self.db)

    def create_seats_object(self):
        return SeatsDataInstanceObjectSQLAlchemy(self.db)

    def create_showings_object(self):
        return ShowingsDataInstanceObjectSQLAlchemy(self.db)

    def create_tickets_object(self):
        return TicketsDataInstanceObjectSQLAlchemy(self.db)

    def create_bookings_object(self):
        return BookingsDataInstanceObjectSQLAlchemy(self.db)

