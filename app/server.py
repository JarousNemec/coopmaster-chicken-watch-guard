import logging

from flask import Flask
from waitress import serve

from app import configuration


def flask_app():
    app = Flask('__main__')

    @app.route("/")
    def hello_world():
        logging.info("Hello World!")
        return configuration.hello_message

    return app

def server(host: str = "127.0.0.1", port: int = 80, ssl: bool = False):
    manager_app = flask_app()

    logging.info("Serving on http://"+configuration.host+":"+str(port))
    serve(manager_app,  port=port)