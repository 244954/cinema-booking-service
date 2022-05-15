from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy


class SeatsDataInstanceObject(ABC):
    @abstractmethod
    def get_seats(self):
        pass


class SeatsDataInstanceObjectSQLAlchemy(SeatsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_seats(self):
        pass
