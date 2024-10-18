import os

host = "127.0.0.1"
port = 9003
hello_message = "Hello from chicken watch guard"

log_file_name = "chicken_watch_guard.log"

def get_log_directory():
    return "./logs/"

def get_log_filename():
    return log_file_name