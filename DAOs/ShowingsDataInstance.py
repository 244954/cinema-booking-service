from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from models.Models import Showings
import datetime

from utils.AlchemyEncoder import AlchemyEncoder


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
    def get_showings(self, from_date, to_date, movie_id, movie_language,
                     dubbing_language, subtitles_language, lector_language, age_limit):
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

    def get_showings(self, from_date, to_date, movie_id, movie_language,
                     dubbing_language, subtitles_language, lector_language, age_limit):
        kwargs = {k: v for k, v in {ShowingsDataInstanceObject.movie_language: movie_language,
                                    ShowingsDataInstanceObject.dubbing_language: dubbing_language,
                                    ShowingsDataInstanceObject.subtitles_language: subtitles_language,
                                    ShowingsDataInstanceObject.lector_language: lector_language}.items() if v is not None}
        from_d = datetime.datetime.fromtimestamp(int(from_date))
        to_d = datetime.datetime.fromtimestamp(int(to_date))
        found_showings = Showings.query.filter(
            and_(Showings.showing_date >= from_d,
                 Showings.showing_date <= to_d,
                 Showings.age_limit <= age_limit,
                 Showings.movie_id == movie_id)).filter_by(
            **kwargs
        ).with_entities(
            Showings.showing_id.label('showing_id'),
            Showings.showing_date.label('showing_date'),
            Showings.movie_id.label('movie_id'),
            Showings.movie_language.label('movie_language'),
            Showings.subtitles.label('subtitles'),
            Showings.dubbing.label('dubbing'),
            Showings.lector.label('lector')
        ).all()

        e = AlchemyEncoder()
        json_list = []
        for u in found_showings:
            data = e.parse_sqlalchemy_object(u)
            for t in data:
                json_list.append(t)
        return json_list

    def insert_showing(self, showing_id, showing_date, hall_id, movie_id, movie_language, age_limit,
                       subtitles, dubbing, lector, subtitles_language, lector_language, dubbing_language):
        showing = Showings(showing_id=showing_id, showing_date=showing_date, hall_id=hall_id, movie_id=movie_id,
                           movie_language=movie_language, age_limit=age_limit, subtitles=subtitles, dubbing=dubbing,
                           lector=lector, subtitles_language=subtitles_language, lector_language=lector_language,
                           dubbing_language=dubbing_language)
        self.db.session.add(showing)

    def commit(self):
        self.db.session.commit()
