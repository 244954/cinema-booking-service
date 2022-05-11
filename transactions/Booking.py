from models.Models import Showings, Tickets_For_Showings
from flask import request, Response, jsonify, make_response
from sqlalchemy import and_, func
from flask_sqlalchemy import SQLAlchemy
from utils.Generators import generate_response
from utils.Response_codes import *
from utils.AlchemyEncoder import AlchemyEncoder
import datetime


def get_showings(db: SQLAlchemy, post_request: request, from_date, to_date, movie_id, movie_language,
                 dubbing_language, subtitles_language, lector_language, age_limit) -> Response:
    message_list = []
    from_date_name = ('from_date', from_date)
    to_date_name = ('to_date', to_date)
    movie_id_name = ('movie_id', movie_id)
    age_limit_name = ('age_limit', age_limit)
    mandatory_parameters = [from_date_name, to_date_name, movie_id_name, age_limit_name]
    for name in mandatory_parameters:
        if name[1] is None:
            return generate_response('Mandatory {} parameter missing'.format(name[0]), Status_code_invalid_data)
    kwargs = {k: v for k, v in {"movie_language": movie_language,
                                "dubbing_language": dubbing_language,
                                "subtitles_language": subtitles_language,
                                "lector_language": lector_language}.items() if v is not None}
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
    jsonlist = []
    for u in found_showings:
        data = e.parse_sqlalchemy_object(u)
        for t in data:
            jsonlist.append(t)
    response_list = {"showings": jsonlist}
    response = make_response(jsonify(response_list), Status_code_ok)
    return response
