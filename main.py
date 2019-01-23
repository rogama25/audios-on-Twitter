import os
import sys
import settings
import telegram
import random
import re
import time
from util import press_enter


def main():
	random.seed()
	cfg = settings.Settings()
	while True:
		try:
			tg = telegram.TGBot(cfg).bot
			print("Bot successfully started. Do CTRL-C to stop.")
			if cfg.telegram_user_id is None:
				link_key = ""
				for i in range (0, 6):
					link_key = link_key + str(random.randint(0,9))
				print("Please send your bot the following code as a Telegram message: " + link_key)
			
			@tg.message_handler(func=lambda msg: True)
			def tg_message_handler(message):
				if cfg.telegram_user_id is None:
					if message.text == link_key:
						cfg.telegram_user_id = message.from_user.id
						print("Bot linked to " + str(message.from_user.id) + " (" + message.from_user.first_name + ")")
						cfg.save_settings("config.cfg")
				else:
					if message.from_user.id == cfg.telegram_user_id:
						match = re.search("https://twitter.com/[a-z|A-Z|0-9|_]+/status/[0-9]+",message.text)
						if match is not None:
							url = message.text[match.start():match.end()]
							foo, tweetid = url.rsplit("/", 1)
							print(tweetid)
		
			tg.polling()
			print("Bot stopped. It may be because you pressed CTRL-C or because an error occurred. Press enter.")
			press_enter()
			cfg.edit_settings()
			
		except ValueError as e:
			print("Error.")
			sys.exit()


if __name__ == "__main__":
	main()
