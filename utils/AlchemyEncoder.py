import json
from decimal import Decimal
from datetime import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, tuple):
            data = {}
            for obj in o:
                data.update(self.parse_sqlalchemy_object(obj))
            return data
        if isinstance(o.__class__, DeclarativeMeta):
            return self.parse_sqlalchemy_object(o)
        return json.JSONEncoder.default(self, o)


    def parse_sqlalchemy_object(self, o):
        data = {}
        fields = o.__json__() if hasattr(o, '__json__') else dir(o)
        for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class', 'count', 'index', 'keys']]:
            value = o.__getattribute__(field)
            try:
                json.dumps(value)
                if field == 'showing_id' or field == 'showing_date' or field == 'movie_id':
                    data[field] = value
                else:
                    data[field] = value
            except TypeError:
                data_type = type(value)
                if data_type is Decimal or data_type is datetime:
                    value = str(value)
                    data[field] = value
                elif data_type is bool:
                    value = bool(value)
                    data[field] = value
        list_of_showings = [data]
        return list_of_showings
