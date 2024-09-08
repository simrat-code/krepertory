#
# flask --app krep run --debug
# uwsgi --ini wsgi.ini
#

import os
from flask import Flask

from . import krepapp
from . import krepconfig


def create_app():
    app = Flask(__name__)

    environment = os.environ.get("FLASK_ENV", default="development")
    cfg = krepconfig.ProductionConfig() if environment == "production" else krepconfig.DevelopmentConfig()
    app.config.from_object(cfg)

    app.register_blueprint(krepapp.bp)

    return app
    