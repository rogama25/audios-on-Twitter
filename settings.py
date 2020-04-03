from util import cls, press_enter, get_config_dir
import sys
import os
import languages
from languages import get_string


class Settings:

    def __init__(self):
        self.telegram_key = None
        self.telegram_user_id = None
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_secret = None
        self.lang = "en"
        if not os.path.exists(get_config_dir() + "config.cfg") and os.path.isfile("config.cfg"):
            if not os.path.isdir(get_config_dir()):
                os.makedirs(get_config_dir())
            os.rename("config.cfg", get_config_dir() + "config.cfg")
        try:
            self.load_file(get_config_dir() + "config.cfg")
        except ValueError as e:
            print("An error occurred while loading settings file.")
            if len(e.args) > 0:
                print(e.args[0])
            press_enter()
            self.edit_settings()

    def load_file(self, file: str):
        """Loads a config file

        :param file: config file URI
        :type file: str
        :return: None
        :raises ValueError: This exception get raised if settings file is corrupt. More information about the error is described on the first attribute
        """
        if os.path.isfile(file):
            with open(file, "r+") as f:
                not_numeric = False
                for line in f:
                    key, value = line.split("=", 1)
                    if value.endswith("\n"):
                        value = value[:-1]
                    if key in list(self.__dict__.keys()):
                        if key != "telegram_user_id":
                            self.__dict__[key] = value
                            if key == "lang":
                                languages.selected = value
                        else:
                            if value.isdigit():
                                self.telegram_user_id = int(value)
                            else:
                                not_numeric = True
                    else:
                        raise ValueError(get_string("settings_corrupt"))
                if not_numeric:
                    raise ValueError(get_string("telegram_notnumeric"))
            if not self.attributes_complete():
                raise ValueError(get_string("missing_settings"))
        else:
            self.language_selector()
            self.edit_settings()

    def edit_settings(self):
        """Shows a command-line editor for the settings

        :return: None
        """
        while True:
            cls()
            print(get_string("settings_info"))
            print(get_string("edit_tg_key").format(1))
            print(get_string("unlink_tg").format(2))
            print(get_string("edit_tw_consumer").format(3))
            print(get_string("edit_tw_access").format(4))
            print(get_string("start_bot").format(5))
            print(get_string("change_language").format(6))
            print(get_string("exit").format(7))
            option = input()
            if option == '1':
                inp = input(get_string("input_tg_key"))
                if inp != '':
                    self.telegram_key = inp
            if option == '2':
                if input(get_string("unlink_tg_confirm")).lower() == 'y':
                    self.telegram_user_id = None
            if option == '3':
                inp = input(get_string("input_tw_consumer"))
                if inp != '':
                    self.consumer_key = inp
                inp = input(get_string("input_tw_consumer_secret"))
                if inp != '':
                    self.consumer_secret = inp
            if option == '4':
                inp = input(get_string("input_tw_access"))
                if inp != '':
                    self.access_token = inp
                inp = input(get_string("input_tw_access_secret"))
                if inp != '':
                    self.access_secret = inp
            if option == '5':
                is_complete, missing = self.attributes_complete(True)
                if is_complete:
                    self.save_settings(get_config_dir() + "config.cfg")
                    return
                else:
                    for attr in missing:
                        attr = attr.replace('_', ' ')
                        attr = attr.capitalize()
                        print(get_string("attribute_missing").format(attr))
                    input(get_string("return_menu"))
            if option == '7':
                if self.attributes_complete():
                    self.save_settings(get_config_dir() + "config.cfg")
                sys.exit()
            if option == '6':
                self.language_selector()

    def save_settings(self, file: str):
        """Saves settings to disk

        :param file: URI of the config file
        :type file: str
        :return: None
        """
        with open(file, "w+") as f:
            for attr, value in self.__dict__.items():
                if value is not None:
                    f.write(attr + "=" + str(value) + "\n")

    def attributes_complete(self, return_values: bool = False):
        """Checks if all the required attributes are set up successfully.

        :param return_values: Returns the missing needed values as an array on the second return object. Defaults to false
        :type return_values: bool
        :return: If return_values is false:
            Returns true if all required attributes are set up. Returns false if not.
            If return_values is true:
            Returns true, array_of_missing_elements_as_strings if everything is ok. Returns false, [] if not.
        """
        missing = []
        for attr, value in self.__dict__.items():
            if value is None:
                if attr is not "telegram_user_id":
                    missing.append(attr)
        if len(missing) == 0:
            if return_values:
                return True, missing
            else:
                return True
        else:
            if return_values:
                return False, missing
            else:
                return False

    def language_selector(self):
        print("Select a language:")
        langs = languages.get_available()
        langcodes = []
        for n, (langcode, langname) in enumerate(langs.items()):
            print("[" + str(n + 1) + "]" + " " + langname)
            langcodes.append(langcode)
        while True:
            string = input("[1-" + str(n + 1) + "?] ")
            try:
                num = int(string)
                if 1 <= num <= len(langs):
                    self.lang = langcodes[num - 1]
                    languages.selected = langcodes[num - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Value is not valid.")
