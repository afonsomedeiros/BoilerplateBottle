from bottle import Bottle
from .routes import create_route


def create_app():
    app = Bottle()

    create_route(app)
    return app
