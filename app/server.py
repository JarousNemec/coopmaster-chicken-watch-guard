import json
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from waitress import serve

from app import configuration
from app.blueprints.admin_blueprint import admin_blueprint
from app.cron.dog_repoter import check_dog


def flask_app():
    app = Flask('__main__')

    app.config['MQTT_BROKER_URL'] = '127.0.0.1'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = 'admin'  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = 'password'  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    @app.route("/")
    def hello_world():
        logging.info("Hello World!")
        return configuration.hello_message

    app.register_blueprint(admin_blueprint)

    return app


def server(host: str = "127.0.0.1", port: int = 80, ssl: bool = False):
    manager_app = flask_app()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_dog, 'interval', seconds=configuration.config.REPORT_INTERVAL)
    scheduler.start()

    logging.info("Serving on http://" + configuration.host + ":" + str(port))
    serve(manager_app, port=port)
