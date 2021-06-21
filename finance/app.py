# -*- coding: utf-8 -*-

import os
from flask import Flask
from .config import app_config


def create_app():
    flask_app = Flask(__name__)
    config_name = os.getenv('APP_SETTINGS')
    flask_app.config.from_object(app_config[config_name])
    flask_app.config.from_pyfile('config.py')
    return flask_app


app = create_app()


if __name__ == '__main__':
    app.run()
