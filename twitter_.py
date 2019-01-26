import twitter
import settings


class Twitter:
	
	def __init__(self,cfg:settings.Settings):
		self.tw = twitter.Api(cfg.consumer_key,cfg.consumer_secret,cfg.access_token,cfg.access_secret,tweet_mode='extended')
		self.reply_id = None
		if self.tw.VerifyCredentials() is None:
			raise ValueError("Twitter credentials are wrong.")
		
	def set_reply(self,reply_id:int):
		try:
			tweet = self.tw.GetStatus(reply_id)
			self.reply_id = reply_id
			return tweet.full_text, tweet.user.screen_name
		except twitter.TwitterError as e:
			return None

	def tweet(self,media:str):
		self.tw.PostUpdate(media=media,in_reply_to_status_id=self.reply_id)
