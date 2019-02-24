import twitter
import settings


class Twitter:
	
	def __init__(self, cfg: settings.Settings):
		self.tw = twitter.Api(cfg.consumer_key, cfg.consumer_secret, cfg.access_token, cfg.access_secret,
							  tweet_mode='extended')
		self.reply_id = None
		if self.tw.VerifyCredentials() is None:
			raise ValueError("Twitter credentials are wrong.")
		self.text = ""
	
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
	
	def set_text(self, text:str):
		self.text = text
	
	def tweet(self, media: str):
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
		
	def media_status(self,media_id: int):
		url = '%s/media/upload.json' % self.tw.upload_url
		
		parameters = {
			'command': 'STATUS',
			'media_id': media_id
		}
		
		resp = self.tw._RequestUrl(url, 'GET', data=parameters)
		data = self.tw._ParseAndCheckTwitter(resp.content.decode('utf-8'))
		
		return data
