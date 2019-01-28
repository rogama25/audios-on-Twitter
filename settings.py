from util import cls, press_enter
import sys
import os


class Settings:
	
	def __init__(self):
		self.telegram_key = None
		self.telegram_user_id = None
		self.consumer_key = None
		self.consumer_secret = None
		self.access_token = None
		self.access_secret = None
		try:
			self.load_file("config.cfg")
		except ValueError as e:
			print("An error occurred while loading settings file.")
			if len(e.args) > 0:
				print(e.args[0])
			press_enter()
			self.edit_settings()
	
	def load_file(self, file: str):
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
						else:
							if value.isdigit():
								self.telegram_user_id = int(value)
							else:
								not_numeric = True
					else:
						raise ValueError("Settings file appears to be corrupt.")
				if not_numeric:
					raise ValueError("Telegram ID was not a numeric and was not saved..")
			if not self.attributes_complete():
				raise ValueError("Missing settings.")
		else:
			self.edit_settings()
	
	def edit_settings(self):
		while True:
			cls()
			print("""Settings editor. Press the following numbers to edit settings.
[1] Edit Telegram bot API key.
[2] Unlink Telegram bot from current user.
[3] Edit Twitter consumer keys.
[4] Edit Twitter access tokens.
[5] Restart bot.
[6] Exit.""")
			option = input()
			if option == '1':
				inp = input("Paste the new bot key (press enter to return without changing): ")
				if inp != '':
					self.telegram_key = inp
			if option == '2':
				if input(
						"Are you sure you want to unlink from the current Telegram user? Press y to unlink:").lower() == 'y':
					self.telegram_user_id = None
			if option == '3':
				inp = input("Paste the new Twitter consumer key (press enter to ask for secret key without changing): ")
				if inp != '':
					self.consumer_key = inp
				inp = input("Paste the new Twitter consumer secret (press enter to return without changing): ")
				if inp != '':
					self.consumer_secret = inp
			if option == '4':
				inp = input("Paste the new Twitter access token (press enter to ask for secret key without changing): ")
				if inp != '':
					self.access_token = inp
				inp = input("Paste the new Twitter access secret (press enter to return without changing): ")
				if inp != '':
					self.access_secret = inp
			if option == '5':
				is_complete, missing = self.attributes_complete(True)
				if is_complete:
					self.save_settings("config.cfg")
					return
				else:
					for attr in missing:
						attr = attr.replace('_', ' ')
						attr = attr.capitalize()
						print(attr + " is missing. Please set it before trying to start the bot.")
					input("Press enter to return to menu.")
			if option == '6':
				if self.attributes_complete():
					self.save_settings("config.cfg")
				sys.exit()
	
	def save_settings(self, file: str):
		with open(file, "w+") as f:
			for attr, value in self.__dict__.items():
				if value is not None:
					f.write(attr + "=" + str(value) + "\n")
	
	def attributes_complete(self, return_values: bool = False):
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
