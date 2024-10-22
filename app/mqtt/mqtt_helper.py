import logging

from app import configuration


def publish(mqtt_client, topic, json_string):
    publish_result = 0
    try:
        logging.info("Mqtt publishing topic: %s, payload: %s" % (topic, json_string))
        publish_result = mqtt_client.publish(topic, json_string.encode())
    except Exception as e:
        print(e)
    finally:
        return publish_result


def get_basic_topic(target_topic):
    return configuration.modul_topic + target_topic

def get_IO_topic(target_topic, is_response_topic=True):
    if is_response_topic:
        return configuration.modul_topic + "/res" + target_topic
    else:
        return configuration.modul_topic + "/req" + target_topic
