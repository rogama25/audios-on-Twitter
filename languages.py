import os
from util import get_lang_dir
import json


def get_available():
    langs = {}
    for filename in os.listdir(get_lang_dir()):
        file = os.path.join(get_lang_dir(), filename)
        if os.path.isfile(file) and file.endswith(".json"):
            with open(file, "r") as fileobject:
                lang_object = json.load(fileobject)
                if "lang_name" in lang_object:
                    langs[filename] = lang_object["lang_name"]
    return langs


class Languages:

    def __init__(self):
        self.selected = None
