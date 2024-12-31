import json
import logging

import torch
import ultralytics
from ultralytics import YOLO
import requests

from app import configuration


def check_dog():
    bird_count = count_chicken()
    mqtt_client = configuration.get_mqtt_client()

    try:
        mqtt_client.connect()
        report_bird_count(mqtt_client, bird_count)
    except:
        logging.error(
            f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server. {configuration.config.MQTT_BROKER}:{configuration.config.MQTT_PORT} {configuration.config.MQTT_TOPIC} ")
    finally:
        mqtt_client.close()


def report_bird_count(mqtt_client, bird_count):
    message = {"bird": bird_count}
    payload = json.dumps(message)

    result = mqtt_client.publish(configuration.config.MQTT_TOPIC, payload.encode())

    logging.info(f"Going to publish following payload to {configuration.config.MQTT_TOPIC}: {payload.encode()}")
    # Check if the message was successfully published
    status = result[0]
    if status == 0:
        logging.info("Nest status reported successfully")
    else:
        logging.error(f"Nest status reported with error {status}")


def count_chicken():
    temp_img_path = get_image()

    model = YOLO("yolo11x")  # Your model should be here after training
    results = model(temp_img_path)  # image you weant to predict on

    bird_count = 0

    for result in results:
        boxes = result.boxes
        names = result.names
        for box in boxes:
            cls = box.cls  # Class ID
            conf = box.conf  # Confidence score for this detection
            # print(f"Detected class ID: {names[int(cls)]}, Confidence: {int(float(conf)*100)}")
            if names[int(cls)] == "bird":
                bird_count += 1

    return bird_count



def get_image():

    url = 'http://127.0.0.1:9001/api/cam1/image'

    try:
        response = requests.get(url)
        response.raise_for_status()
        image = 'image.jpg'
        with open(image, 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
            file.close()

        return image
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the HTTP request
        print(f"An error occurred: {e}")
