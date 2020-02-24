import os
from util import get_lang_dir
import json

selected = "en"
loaded_langs = {}


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


def get_loaded():
    global loaded_langs
    l = []
    for e in loaded_langs:
        l.append(e)
    return l


def get_string(string, lang = None):
    if lang is None:
        global selected
        lang = selected
    if lang in get_loaded():
        global loaded_langs
        return loaded_langs[lang].strings[string]
    if lang in get_available():
        l = Language(lang)
        return l.strings[string]
    else:
        return get_string(string, "en")


class Language:

    def __init__(self, name):
        if name in get_loaded():
            raise NameError("Language already loaded.")
        if name not in get_available():
            raise NameError("Language not available.")
        self.name = name
        filename = os.path.join(get_lang_dir(), name + ".json")
        with open(filename, "r") as file:
            self.strings = json.load(file)
        global loaded_langs
        loaded_langs[name] = self
