import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from waitress import serve

from app import configuration
from app.blueprints.admin_blueprint import admin_blueprint
from app.cron.chicken_repoter import check_dog


def flask_app():
    app = Flask('__main__')

    @app.route("/")
    def hello_world():
        message = "Chicken Watch Guard"
        logging.info(message)
        return message

    app.register_blueprint(admin_blueprint)

    return app


def server():
    manager_app = flask_app()
    port = configuration.config.PORT
    host = configuration.config.HOST

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_dog, 'interval', seconds=configuration.config.REPORT_INTERVAL)
    scheduler.start()

    logging.info(f"Serving on http://{host}:{port}")
    serve(manager_app, port=port)
