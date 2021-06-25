from flask import Flask
from flask_restful import Api
from decouple import config as env

from app.main.config import config_by_name, cache
from app.main.controller.stocks import StocksController


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name[env('YAHOO_STOCKS_API_ENV')])

    cache.init_app(app)

    api = Api(app)
    api.add_resource(StocksController, "/stocks")

    return app
