from app import configuration

from app.logging.hen_logger import init_logger
from app.server import server

init_logger()

def start_server():
    server(host=configuration.host, port=configuration.port)


if __name__ == '__main__':
    print(configuration.hello_message)
    start_server()