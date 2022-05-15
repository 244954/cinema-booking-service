from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from models.Models import Showings


class ShowingsDataInstanceObject(ABC):
    showing_id = 'showing_id'
    showing_date = 'showing_date'
    hall_id = 'hall_id'
    movie_id = 'movie_id'
    movie_language = 'movie_language'
    age_limit = 'age_limit'

    subtitles = 'subtitles'
    dubbing = 'dubbing'
    lector = 'lector'
    subtitles_language = 'subtitles_language'
    lector_language = 'lector_language'
    dubbing_language = 'dubbing_language'

    @abstractmethod
    def get_showing(self, showing_id):
        pass

    @abstractmethod
    def insert_showing(self, showing_id, showing_date, hall_id, movie_id, movie_language, age_limit,
                       subtitles, dubbing, lector, subtitles_language, lector_language, dubbing_language):
        pass

    @abstractmethod
    def commit(self):
        pass


class ShowingsDataInstanceObjectSQLAlchemy(ShowingsDataInstanceObject):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_showing(self, showing_id):
        found_showing = Showings.query.filter_by(showing_id=showing_id).first()
        if found_showing:
            return {
                ShowingsDataInstanceObject.showing_id: found_showing.showing_id,
                ShowingsDataInstanceObject.showing_date: found_showing.showing_date,
                ShowingsDataInstanceObject.hall_id: found_showing.hall_id,
                ShowingsDataInstanceObject.movie_id: found_showing.movie_id,
                ShowingsDataInstanceObject.movie_language: found_showing.movie_language,
                ShowingsDataInstanceObject.age_limit: found_showing.age_limit,
                ShowingsDataInstanceObject.subtitles: found_showing.subtitles,
                ShowingsDataInstanceObject.dubbing: found_showing.dubbing,
                ShowingsDataInstanceObject.lector: found_showing.lector,
                ShowingsDataInstanceObject.subtitles_language: found_showing.subtitles_language,
                ShowingsDataInstanceObject.lector_language: found_showing.lector_language,
                ShowingsDataInstanceObject.dubbing_language: found_showing.dubbing_language
            }
        else:
            return None

    def insert_showing(self, showing_id, showing_date, hall_id, movie_id, movie_language, age_limit,
                       subtitles, dubbing, lector, subtitles_language, lector_language, dubbing_language):
        showing = Showings(showing_id=showing_id, showing_date=showing_date, hall_id=hall_id, movie_id=movie_id,
                           movie_language=movie_language, age_limit=age_limit, subtitles=subtitles, dubbing=dubbing,
                           lector=lector, subtitles_language=subtitles_language, lector_language=lector_language,
                           dubbing_language=dubbing_language)
        self.db.session.add(showing)

    def commit(self):
        self.db.session.commit()
