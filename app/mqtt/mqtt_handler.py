import json
import logging
import random

from app import configuration
from app.mqtt import mqtt_helper


def handle_subscribe(mqtt_client, data):
    request_count_topic = mqtt_helper.get_topic(configuration.count_topic, False)
    response_count_topic = mqtt_helper.get_topic(configuration.count_topic)
    if data["topic"] == request_count_topic and data["payload"] == "":
        values = [12, 2, 8, 4, 7, 6, 10]
        chicken_count = random.choice(values)
        payload = json.dumps({"count": chicken_count})
        mqtt_helper.publish(mqtt_client, response_count_topic, payload)