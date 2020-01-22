import twitter
import settings
import time


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
        cuentabot = self.tw.VerifyCredentials()
        if cuentabot is None:
            raise ValueError("Twitter credentials are wrong.")
        self.cuenta = cuentabot.screen_name
        print("Connected to Twitter: " + cuentabot.screen_name)
        self.text = ""
        self.dm_user = None

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
        if self.dm_user is None:
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
            self.tw.PostUpdate(media=video_id, in_reply_to_status_id=self.reply_id, status=self.text,
                               auto_populate_reply_metadata=autopop)
            self.set_text("")
        else:
            fr = self.tw.ShowFriendship(source_screen_name=self.cuenta, target_screen_name=self.dm_user)
            if fr["relationship"]["source"]["can_dm"] == True:
                self.send_dm(self.text, screen_name=self.dm_user, media_file_path=media, media_type="dm_video")
            else:
                raise KeyError()

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

    def send_dm(self,
                text,
                user_id=None,
                media_file_path=None,
                media_type=None,
                screen_name=None,
                return_json=False):
        """Post a twitter direct message from the authenticated user.

        Args:
        text: The message text to be posted.
        user_id:
            The ID of the user who should receive the direct message.
        media_file_path:
            The file path to the media to be posted
        media_type:
            The media type. Accepted media types: dm_image, dm_gif or dm_video
        return_json (bool, optional):
            If True JSON data will be returned, instead of twitter.DirectMessage
        Returns:
            A twitter.DirectMessage instance representing the message posted
        """
        url = '%s/direct_messages/events/new.json' % self.tw.base_url
        # Hack to allow some sort of backwards compatibility with older versions
        # part of the fix for Issue #587
        if user_id is None and screen_name is not None:
            user_id = self.tw.GetUser(screen_name=screen_name).id

        # Default
        message_data_value = {
            'text': text
        }
        if media_file_path is not None:
            if not isinstance(media_file_path, int):
                try:
                    media = open(media_file_path, 'rb')
                except IOError:
                    raise twitter.TwitterError({'message': 'Media file could not be opened.'})

                response_media_id = self.tw.UploadMediaChunked(media=media, media_category=media_type)

            while True:
                data = self.media_status(response_media_id)
                if data['processing_info']['state'] != 'pending' and data['processing_info']['state'] != 'in_progress':
                    break
                time.sleep(1)
            # With media
            message_data_value = {
                'text': text,
                "attachment": {
                    "type": "media",
                    "media": {
                        "id": response_media_id
                    }
                }
            }

        event = {
            'event': {
                'type': 'message_create',
                'message_create': {
                    'target': {
                        'recipient_id': user_id
                    },
                    'message_data': message_data_value
                }
            }
        }

        resp = self.tw._RequestUrl(url, 'POST', json=event)
        data = self.tw._ParseAndCheckTwitter(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            dm = twitter.DirectMessage(
                created_at=data['event']['created_timestamp'],
                id=data['event']['id'],
                recipient_id=data['event']['message_create']['target']['recipient_id'],
                sender_id=data['event']['message_create']['sender_id'],
                text=data['event']['message_create']['message_data']['text'],
            )
            dm._json = data
            return dm

    def set_dm_user(self, user: str):
        try:
            self.tw.GetUser(screen_name=user)
        except:
            self.dm_user = None
        self.dm_user = user
        return self.dm_user
