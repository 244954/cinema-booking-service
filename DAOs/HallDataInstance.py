from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Halls


class HallsDataInstanceObject(ABC):
    hall_id = 'hall_id'
    cinema_id = 'cinema_id'
    hall_name = 'hall_name'

    @abstractmethod
    def get_hall(self, hall_id):
        pass

    @abstractmethod
    def insert_hall(self, hall_id, cinema_id, hall_name):
        pass

    @abstractmethod
    def commit(self):
        pass


class HallsDataInstanceObjectSQLAlchemy(HallsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_hall(self, hall_id):
        found_hall = Halls.query.filter_by(hall_id=hall_id).first()
        if found_hall:
            return {
                HallsDataInstanceObject.hall_id: found_hall.hall_id,
                HallsDataInstanceObject.cinema_id: found_hall.cinema_id,
                HallsDataInstanceObject.hall_name: found_hall.hall_name
            }
        else:
            return None

    def insert_hall(self, hall_id, cinema_id, hall_name):
        hall = Halls(hall_id=hall_id, cinema_id=cinema_id, hall_name=hall_name)
        self.db.session.add(hall)

    def commit(self):
        self.db.session.commit()
