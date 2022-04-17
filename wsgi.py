from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS, cross_origin
from models.Models import db
from utils.Response_codes import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Spanko123@localhost/cinema-booking-service'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'NOT IMPLEMENTED'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)


@app.route('/booking', methods=['POST'])
def booking():
    if request.method == 'POST':
        return Response(status=Status_code_ok)
    else:
        return Response(status=Status_code_not_found)


if __name__ == '__main__':
    with app.app_context():
        #  db.drop_all()
        db.create_all()
        app.run(debug=True)
