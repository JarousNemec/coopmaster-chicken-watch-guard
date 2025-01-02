import json
import logging
import requests

from app import configuration
from app.configuration import model


def check_dog():
    bird_count, actual_image = count_chicken()
    mqtt_client = configuration.get_mqtt_client()

    try:
        mqtt_client.connect()
        report_chicken_count(mqtt_client, bird_count)
        report_actual_image(mqtt_client, actual_image)
    except:
        logging.error(
            f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server. {configuration.config.MQTT_BROKER}:{configuration.config.MQTT_PORT} {configuration.config.MQTT_TOPIC} ")
    finally:
        mqtt_client.close()


def report_actual_image(mqtt_client, actual_image):
    with open(actual_image, "rb") as image_file:
        image_bytes = image_file.read()

        result = mqtt_client.publish(configuration.config.MQTT_CHICKEN_ACTUAL_IMAGE, image_bytes)

        logging.info(
            f"Going to publish following payload to {configuration.config.MQTT_CHICKEN_ACTUAL_IMAGE}: {len(image_bytes)}")
        # Check if the message was successfully published
        status = result[0]
        if status == 0:
            logging.info("Chicken room actual image reported successfully")
        else:
            logging.error(f"Chicken room actual image reported with error {status}")


def report_chicken_count(mqtt_client, bird_count):
    message = {"bird": bird_count}
    payload = json.dumps(message)

    result = mqtt_client.publish(configuration.config.MQTT_CHICKEN_COUNT_TOPIC, payload.encode())

    logging.info(
        f"Going to publish following payload to {configuration.config.MQTT_CHICKEN_COUNT_TOPIC}: {payload.encode()}")
    # Check if the message was successfully published
    status = result[0]
    if status == 0:
        logging.info("Chicken count reported successfully")
    else:
        logging.error(f"Chicken count reported with error {status}")


def count_chicken():
    temp_img_path = get_image()

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

    return bird_count, temp_img_path


def get_image():
    host = configuration.config.CHICKEN_CAMERA_HOST
    port = configuration.config.CHICKEN_CAMERA_PORT

    url = f'http://{host}:{port}/api/chicken/image'

    try:
        response = requests.get(url)
        response.raise_for_status()
        image = 'chicken.jpg'
        with open(image, 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
            file.close()

        return image
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the HTTP request
        print(f"An error occurred: {e}")
