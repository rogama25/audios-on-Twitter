from main import cls
import sys


class Settings:
	telegram_key = None
	telegram_user_id = None
	consumer_key = None
	consumer_secret = None
	access_token = None
	access_secret = None
	
	def __init__(self):
		try:
			self.load_file("config.cfg")
		except ValueError:
			print("An error occurred while loading settings file.")
			self.edit_settings()
	
	def load_file(self, file: str):
		with open(file, "r+") as f:
			for line in f:
				key, value = line.split("=", 1)
				if value.endswith("\n"):
					value = value[:-1]
				if key in list(self.__dict__.keys()):
					self.__dict__[key] = value
				else:
					raise ValueError("Settings file appears to be corrupt.")
		for attr, value in self.__dict__.items():
			if value is None:
				if attr is not "telegram_user_id":
					raise ValueError("Missing settings.")
	
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
					return
				else:
					for attr in missing:
						attr.replace('_', ' ')
						attr.capitalize()
						print(attr + " is missing. Please set it before trying to start the bot.")
			if option == '6':
				if self.attributes_complete():
					self.save_settings("config.cfg")
				sys.exit()
	
	def save_settings(self, file: str):
		with open(file, "w+") as f:
			for attr, value in self.__dict__.items():
				if value is not None:
					f.write(attr + "=" + value)
	
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
