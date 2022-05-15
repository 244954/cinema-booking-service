import py_eureka_client.eureka_client as eureka_client
from eureka.config import *

eureka_client.init(eureka_server=EUREKA_SERVER_NAME,
                   app_name=APP_NAME)
