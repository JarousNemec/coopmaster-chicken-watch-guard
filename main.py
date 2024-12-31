from app import configuration

from app.logging.hen_logger import init_logger
from app.server import server

init_logger()


def start_server():
    server()


if __name__ == '__main__':
    print("Hello from chicken watch guard!")
    start_server()
