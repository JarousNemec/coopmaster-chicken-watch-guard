import json
import logging
import random

from flask_mqtt import Mqtt
from flask import Flask, request, jsonify
from waitress import serve

from app import configuration
from app.cron.timer import start_cron
from app.mqtt import mqtt_helper


def flask_app():
    app = Flask('__main__')

    app.config['MQTT_BROKER_URL'] = '127.0.0.1'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = 'admin'  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = 'password'  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client = Mqtt(app)

    @app.route("/")
    def hello_world():
        logging.info("Hello World!")
        return configuration.hello_message

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info('Connected successfully')
            mqtt_client.subscribe(configuration.wildcard_modul_topic)  # subscribe topic
        else:
            logging.info('Bad connection. Code:', rc)

    # @mqtt_client.on_topic(mqtt_helper.get_topic(configuration.count_topic, False))
    # def handle_chicken_count_request(client, userdata, message):
    #     response_count_topic = mqtt_helper.get_topic(configuration.count_topic)
    #     values = [12, 2, 8, 4, 7, 6, 10]
    #     chicken_count = random.choice(values)
    #     payload = json.dumps({"count": chicken_count})
    #     mqtt_helper.publish(mqtt_client, response_count_topic, payload)

    # @mqtt_client.on_message()
    # def log_subscribed_message(client, userdata, message):
    #     data = dict(
    #         topic=message.topic,
    #         payload=message.payload.decode()
    #     )
    #     logging.info("Mqtt subscribed topic: %s, payload: %s" % (data['topic'], data['payload']))

    @app.route('/publish', methods=['POST'])
    def publish_message():
        request_data = request.get_json()
        publish_result = mqtt_helper.publish(mqtt_client, request_data['topic'], request_data['msg'])
        return jsonify({'code': publish_result[0]})

    return app, mqtt_client


def server(host: str = "127.0.0.1", port: int = 80, ssl: bool = False):
    manager_app, mqtt_client = flask_app()
    start_cron(manager_app.config, mqtt_client)
    logging.info("Serving on http://" + configuration.host + ":" + str(port))
    serve(manager_app, port=port)
