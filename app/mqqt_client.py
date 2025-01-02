import logging

import paho.mqtt.client as mqtt


class NestMQTTClient:
    def __init__(self, broker, port, username, password):
        self.broker = broker
        self.port = port
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(username, password)

    def connect(self):
        self.mqtt_client.connect(self.broker, self.port, 60)
        self.mqtt_client.loop_start()

    def publish(self, topic, payload):
        return self.mqtt_client.publish(topic, payload)

    def on_connect(self, client, userdata, flags, rc):
        pass

    # Definice callback funkce při přijetí zprávy
    def on_message(self, client, userdata, msg):
        pass

    def close(self):
        self.mqtt_client.disconnect()
