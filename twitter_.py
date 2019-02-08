import twitter
import settings


class Twitter:
	
	def __init__(self, cfg: settings.Settings):
		self.tw = twitter.Api(cfg.consumer_key, cfg.consumer_secret, cfg.access_token, cfg.access_secret,
							  tweet_mode='extended')
		self.reply_id = None
		if self.tw.VerifyCredentials() is None:
			raise ValueError("Twitter credentials are wrong.")
	
	def set_reply(self, reply_id: int):
		if reply_id is not None:
			try:
				tweet = self.tw.GetStatus(reply_id)
				self.reply_id = int(reply_id)
				return tweet.full_text, tweet.user.screen_name
			except twitter.TwitterError as e:
				return None, None
		else:
			self.reply_id = None
			return None, None
	
	def tweet(self, media: str):
		if self.reply_id is None:
			autopop = False
		else:
			autopop = True
		self.tw.PostUpdate(media=media, in_reply_to_status_id=self.reply_id, status="", auto_populate_reply_metadata=autopop)
