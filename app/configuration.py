import os

host = "127.0.0.1"
port = 9003
hello_message = "Hello from chicken watch guard"

log_file_name = "chicken_watch_guard.log"

modul_topic = "/chicken_watch_guard"
wildcard_modul_topic = "/chicken_watch_guard/#"
count_topic = "/count"
image_topic = "/image"

def get_log_directory():
    return "./logs/"

def get_log_filename():
    return log_file_name