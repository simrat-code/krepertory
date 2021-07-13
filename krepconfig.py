	
import logging
from os import environ
from os import urandom
 
class Config(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
 
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get("APP_SECRET_KEY", default=str(urandom(16).hex()))
 
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'INSECURE_LOCALDEV_' + str(urandom(8).hex())
 
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False