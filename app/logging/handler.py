import asyncio
import os
import sys
import logging
import colorama

WINDOWS = (sys.platform.startswith("win") or (sys.platform == 'cli' and os.name == 'nt'))


def _color_wrap(*colors):
    def wrapped(inp):
        return "".join(list(colors) + [inp, colorama.Style.RESET_ALL])

    return wrapped


OriginalStreamHandler = logging.StreamHandler


class NewStreamHandler(logging.StreamHandler):

    def __init__(self, stream=None):
        OriginalStreamHandler.__init__(self, stream)

    def format(self, record: logging.LogRecord) -> str:
        try:
            task = asyncio.current_task()
            state = ""
            try:
                state = task._state[0]
            except:
                pass

            record.currentTask = f"{task.get_name()} [{state}]"
        except:
            record.currentTask = None
        return super().format(record)


logging.StreamHandler = NewStreamHandler


class ColorizedStreamHandler(logging.StreamHandler):
    # Don't build up a list of colors if we don't have colorama
    if colorama:
        COLORS = [
            # This needs to be in order from highest logging level to lowest.
            (logging.ERROR, _color_wrap(colorama.Fore.RED)),
            (logging.WARNING, _color_wrap(colorama.Fore.YELLOW)),
            (logging.INFO, _color_wrap(colorama.Fore.WHITE)),
            (logging.DEBUG, _color_wrap(colorama.Fore.CYAN)),
        ]
    else:
        COLORS = []

    def __init__(self, stream=None):
        super(ColorizedStreamHandler, self).__init__(stream)

        if WINDOWS and colorama:
            self.stream = colorama.AnsiToWin32(self.stream)

    @property
    def should_color(self):
        return True if colorama else False

    def format(self, record):
        msg = logging.StreamHandler.format(self, record)

        if self.should_color:
            for level, color in self.COLORS:
                if record.levelno >= level:
                    msg = color(msg)
                    break

        return msg
