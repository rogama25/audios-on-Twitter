import os
import sys
import settings
import telegram
import random
import re
import twitter_
from util import press_enter
import converter


def main():
	random.seed()
	cfg = settings.Settings()
	while True:
		try:
			tgclass = telegram.TGBot(cfg)
			tg = tgclass.bot
			tw = twitter_.Twitter(cfg)
			print("Bot successfully started. Do CTRL-C to stop.")
			if cfg.telegram_user_id is None:
				link_key = ""
				for i in range (0, 6):
					link_key = link_key + str(random.randint(0,9))
				print("Please send your bot the following code as a Telegram message: " + link_key)
			
			@tg.message_handler(content_types=['voice'])
			def tg_audio_handler(message):
				if message.from_user.id == cfg.telegram_user_id:
					tgclass.send_msg("We received the voice note. Please wait a few seconds while we sent it to Twitter. Please don't send me anything else till you receive a reply from me.")
					voice_info = tg.get_file(message.voice.file_id)
					downloaded_voice = tg.download_file(voice_info.file_path)
					if not os.path.exists("media"):
						os.makedirs("media")
					filename = "media/"+str(message.voice.file_id)
					duration = message.voice.duration
					with open(filename+".ogg", "wb") as file:
						file.write(downloaded_voice)
					converter.convert(filename,duration)
					tw.tweet(filename + ".mp4")
					tgclass.send_msg("Audio sent.")
					os.remove(filename + ".ogg")
					os.remove(filename + ".mp4")
			
			@tg.message_handler(func=lambda msg: True)
			def tg_message_handler(message):
				if cfg.telegram_user_id is None:
					if message.text == link_key:
						cfg.telegram_user_id = message.from_user.id
						print("Bot linked to " + str(message.from_user.id) + " (" + message.from_user.first_name + ")")
						tgclass.send_msg("Bot successfully linked. You can send me voice notes and I will Tweet them as a video or send me a link to a Tweet and then the voice note and I will tweet them as a reply to the specified Tweet.")
						cfg.save_settings("config.cfg")
				else:
					if message.from_user.id == cfg.telegram_user_id:
						match = re.search("https://twitter.com/[a-z|A-Z|0-9|_]+/status/[0-9]+",message.text)
						if match is not None:
							url = message.text[match.start():match.end()]
							foo, tweet_id = url.rsplit("/", 1)
							print(tweet_id)
							tweet_text, user = tw.set_reply(tweet_id)
							if tweet_text is not None:
								tgclass.send_msg("Now replying to: @" + user + ": " + tweet_text + "\nTo post the audio as a tweet instead of a reply, send \"/cancel\"")
							else:
								tgclass.send_msg("The tweet you sent seems to not exist.")
						else:
							if message.text == "/cancel":
								tw.set_reply(None)
								tgclass.send_msg("Now posting as a Tweet.")
		
			tg.polling()
			print("Bot stopped. It may be because you pressed CTRL-C or because an error occurred. Press enter.")
			press_enter()
			cfg.edit_settings()
			
		except ValueError as e:
			print("Error. " + e.args)
			sys.exit()


if __name__ == "__main__":
	main()
