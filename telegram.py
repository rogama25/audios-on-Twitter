import telebot
from telebot.apihelper import ApiException
import settings


class TGBot:
	
	def __init__(self, cfg: settings.Settings):
		self.key = cfg.telegram_key
		self.user = cfg.telegram_user_id
		self.bot = telebot.TeleBot(self.key)
		try:
			self.bot.get_me()
		except ApiException:
			raise ValueError("Invalid Telegram API key.")
