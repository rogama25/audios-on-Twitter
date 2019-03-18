import telebot
from telebot.apihelper import ApiException
import settings


class TGBot:
	"""This is the Telegram Bot class
	
	Attributes:
		:ivar key: Telegram API key
		:ivar user: Telegram user ID that the bot is linked to
		:ivar bot: The pyTelegramBotAPI bot instance
		:type key: str
		:type user: int
		:type bot: TeleBot
	"""
	
	def __init__(self, cfg: settings.Settings):
		"""Inits the bot and tests that the API key is valid.
		
		:param cfg: configurations class
		:type cfg: Settings
		"""
		self.key = cfg.telegram_key
		self.user = cfg.telegram_user_id
		self.bot = telebot.TeleBot(self.key)
		try:
			cuentabot = self.bot.get_me()
		except ApiException:
			raise ValueError("Invalid Telegram API key.")
		print("Connected to Telegram: " + cuentabot.username)
	
	def send_msg(self, text:str):
		"""Sends a Telegram message to the linked user
		
		:param text: Text message
		:type text: str
		:return: None
		"""
		self.bot.send_message(self.user,text)
