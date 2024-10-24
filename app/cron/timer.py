import json
import logging
import random
from datetime import datetime

import cv2

from apscheduler.schedulers.background import BackgroundScheduler

from app import configuration
from app.mqtt import mqtt_helper


def publish_current_count(cfg, mqtt_client, topic):
    logging.info("Starting task publish_current_count")
    values = [12, 2, 8, 4, 7, 6, 10]
    chicken_count = random.choice(values)
    payload = json.dumps({"count": chicken_count})
    mqtt_helper.publish(mqtt_client, topic, payload)

def publish_current_image(cfg, mqtt_client, topic):
    cam = cv2.VideoCapture("C:/Users/mortar/PycharmProjects/CoopMaster_modules/chicken_watch_guard/app/cron/Kvok.mp4")
    currentframe = 1

    success = True
    while success:
        success, frame = cam.read()

        if currentframe%30 == 0 and frame is not None:
            _, frame_buff = cv2.imencode('.png', frame)
            mqtt_client.publish(topic, frame_buff.tobytes())
            logging.info("publish_current_image - sending")
        currentframe += 1

    cam.release()


def start_cron(cfg, mqtt_client):
    scheduler = BackgroundScheduler()

    interval = 10
    chicken_count_topic = mqtt_helper.get_basic_topic(configuration.count_topic)
    scheduler.add_job(lambda: publish_current_count(cfg, mqtt_client, chicken_count_topic), 'interval', seconds=interval)

    # interval = 360
    image_topic = mqtt_helper.get_basic_topic(configuration.image_topic)
    scheduler.add_job(lambda: publish_current_image(cfg, mqtt_client, image_topic), 'date', next_run_time=datetime.now())

    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.start()
