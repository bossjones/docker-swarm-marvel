import sys
from termcolor import cprint


# TODO - COMMON ABSTRACT CLASS NEEDED THIS IS HORRIBLE


class Logger:
    def __init__(self, level=None):
        self.level = level
        self.printed = 0
        self.prepend = ""

    def reset(self):
        self.printed = 0

    def _prepare_message(self, msg):
        return self.prepend + msg

    def title(self, msg):
        self.printed += 1
        cprint(self._prepare_message(msg), attrs=["underline", "bold"])

    def bold(self, msg):
        self.printed += 1
        cprint(self._prepare_message(msg), attrs=["bold"])

    def debug(self, msg):
        if self.level:
            self.printed += 1
            cprint(self._prepare_message(msg), "cyan")

    def warn(self, msg):
        self.printed += 1
        cprint(self._prepare_message(msg), "yellow")

    def info(self, msg):
        self.printed += 1
        cprint(self._prepare_message(msg), "green")

    def text(self, msg):
        sys.stdout.write(self._prepare_message(msg))

    def error(self, msg):
        self.printed += 1
        cprint(self._prepare_message(msg), "red")

    def remove_last_line(self):
        if self.level <= 0:
            self.printed -= 1
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

    def clear(self, number=-1):
        if self.level <= 0:
            if number < 0:
                number = self.printed
            for i in range(number):
                self.remove_last_line()
            self.printed = 0


import termcolor


class ListLogger:
    _color_map = {
        "debug": "cyan",
        "warn": "yellow",
        "error": "red",
        "info": "green"
    }

    _attr_map = {
        "title": ["bold", "underline"],
        "bold": ["bold"]
    }

    def __init__(self, level=None):
        self.level = level
        self.clear()
        self.prepend = ""

    def reset(self):
        pass

    def remove_last_line(self):
        del(self.logs[len(self.logs) - 1])

    def clear(self):
        self.lines = []

    def __getattr__(self, name):
        if not (name in self._color_map or name in self._attr_map):
            raise NotImplementedError
        if name == "debug" and self.level < 1:
            return lambda msg: self.prepend + msg
        if name == "text":
            return lambda msg: self.lines.append(prepend + msg)
        color = self._color_map[name] if name in self._color_map else None
        attrs = self._attr_map[name] if name in self._attr_map else None
        return lambda msg: self.lines.append(prepend + "%s\n"
                                             % termcolor.colored(msg, color, None, attrs))
