SECRET_KEY = 'secret!'
env = 'dev'
SQLALCHEMY_DATABASE_URI_DEV = 'postgresql://postgres:Spanko123@localhost/cinema-booking-service'
SQLALCHEMY_DATABASE_URI_PROD = 'postgres://zvbrepbrzinmob' \
                               ':353756c35468cb6c43a142b686d2f9120dfcc88968d95aeeb7a0e33fbcb5c542@ec2-52-18-116-67.eu' \
                               '-west-1.compute.amazonaws.com:5432/dddakce3tomshd '
SQLALCHEMY_TRACK_MODIFICATIONS = False
CORS_HEADERS = 'Content-Type'
