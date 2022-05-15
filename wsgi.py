from threading import Thread
from flask_app import *
from eureka import *  # unused, but don't delete
from mqrabbit import *
from utils.Others import drop_everything


if __name__ == '__main__':
    with app.app_context():
        #  drop_everything(db)
        #  db.create_all()
        thread = Thread(target=channel_cancel_reservation_receive.start_consuming)
        thread.start()
        app.run(debug=True)
