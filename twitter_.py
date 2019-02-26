import twitter
import settings


class Twitter:
	"""This is the Twitter API class
	
	Attributes:
		:ivar tw: API of python-twitter
		:ivar reply_id: The tweet id that the next audios will be in reply to.
		:ivar text: The text for the next Tweet
	
	"""
	
	def __init__(self, cfg: settings.Settings):
		"""Configures the Twitter class and checks that the API key is valid
		
		:param cfg: Settings class
		:type cfg: Settings
		"""
		self.tw = twitter.Api(cfg.consumer_key, cfg.consumer_secret, cfg.access_token, cfg.access_secret,
							  tweet_mode='extended')
		self.reply_id = None
		if self.tw.VerifyCredentials() is None:
			raise ValueError("Twitter credentials are wrong.")
		self.text = ""
	
	def set_reply(self, reply_id: int):
		"""Sets the tweet that the next audios will be in reply to.
		
		:param reply_id: tweet id
		:type reply_id: int
		:return: text_of_the_tweet, username as strings if the tweet is reachable or None, None if it's not, or the reply_id is None.
		"""
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
	
	def set_text(self, text: str):
		"""Sets the text for the next Tweet
		
		:param text: Text
		:type text: str
		:return: None
		"""
		self.text = text
	
	def tweet(self, media: str):
		"""Tweets the audio
		
		:param media: video filename (including extension)
		:type media: str
		:return: None
		"""
		if self.reply_id is None:
			autopop = False
		else:
			autopop = True
		video_id = self.tw.UploadMediaChunked(media, media_category="tweet_video")
		import time
		while True:
			data = self.media_status(video_id)
			if data['processing_info']['state'] != 'pending' and data['processing_info']['state'] != 'in_progress':
				break
			time.sleep(1)
		self.tw.PostUpdate(media=video_id, in_reply_to_status_id=self.reply_id, status=self.text, auto_populate_reply_metadata=autopop)
		self.set_text("")
		
	def media_status(self, media_id: int):
		"""Checks the status of the uploaded media before tweeting
		
		:param media_id: media_id, obtained through the Twitter API
		:type media_id: int
		:return: data dictionary
		:rtype: dict
		"""
		url = '%s/media/upload.json' % self.tw.upload_url
		
		parameters = {
			'command': 'STATUS',
			'media_id': media_id
		}
		
		resp = self.tw._RequestUrl(url, 'GET', data=parameters)
		data = self.tw._ParseAndCheckTwitter(resp.content.decode('utf-8'))
		
		return data
