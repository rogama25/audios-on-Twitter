import os
import sys


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


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
				raise ValueError("Missing settings")

	def edit_settings(self):
		pass

# def main():
#
#
#
# if __name__ == "__main__":
# 	main()
