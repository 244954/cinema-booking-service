from threading import Thread
from flask_app import *
from eureka import *  # unused, but don't delete
from utils.Others import drop_everything


if __name__ == '__main__':
    with app.app_context():
        #  drop_everything(db)
        #  db.create_all()
        thread = Thread(target=rabbit_channels.start_mqrabbit)
        thread.start()
        app.run(debug=True)
