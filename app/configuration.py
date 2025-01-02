import os
from typing import get_type_hints, Union
from ultralytics import YOLO

from flask.cli import load_dotenv

from app.mqqt_client import NestMQTTClient

log_file_name = "chicken_watch_guard.log"

load_dotenv()

def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


class AppConfigError(Exception):
    pass


class AppConfig:
    PORT: int = 10000
    HOST: str = "127.0.0.1"
    CHICKEN_CAMERA_PORT: int = 9001
    CHICKEN_CAMERA_HOST: str = "localhost"

    MQTT_BROKER: str = "192.168.1.177"
    MQTT_PORT: int = 1883
    MQTT_CHICKEN_COUNT_TOPIC: str = "coopmaster/chicken/count"
    MQTT_CHICKEN_ACTUAL_IMAGE: str = "coopmaster/chicken/image/actual"
    MQTT_USERNAME: str = "admin"
    MQTT_PASSWORD: str = "password"
    REPORT_INTERVAL: int = 5

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """

    def __init__(self, env):

        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )
                )

    def __repr__(self):
        return str(self.__dict__)


config = AppConfig(os.environ)
model = YOLO("yolo11x")  # Your model should be here after training


def get_mqtt_client():
    return NestMQTTClient(
        config.MQTT_BROKER,
        config.MQTT_PORT,
        config.MQTT_USERNAME,
        config.MQTT_PASSWORD
    )


def get_log_directory():
    return "./logs/"


def get_log_filename():
    return log_file_name