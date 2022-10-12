#

import importlib.resources


def text(name: str):
    text = importlib.resources.read_text(__package__, name)
    return text
