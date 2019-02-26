import os
import ffmpy


def convert(input_file: str, duration: float):
	"""Converts a ogg audio downloaded from Telegram into a video with a speaker
	
	:param input_file: filename without extension
	:param duration: duration of the audio
	:type input_file: str
	:type duration: float
	:return: None
	"""
	if not os.path.exists("media/img.png"):
		import urllib.request
		urllib.request.urlretrieve("https://raw.githubusercontent.com/rogama25/audios-on-Twitter/master/media/img.png", "media/img.png")
	ff = ffmpy.FFmpeg(
		inputs={'media/img.png': None, input_file + '.ogg': None},
		outputs={input_file + '.mp4': '-c:v libx264 -c:a aac -tune stillimage -pix_fmt yuv420p -vf tpad=stop_mode=clone:stop_duration=' + str(duration)},
		global_options="-loglevel 0"
	)
	ff.run()
