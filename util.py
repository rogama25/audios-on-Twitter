import os
import getpass


def cls():
	"""Clears the console output.
	
	:return: None
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
	"""Waits for the next enter keypress.
	
	:return: None
	"""
	getpass.getpass(prompt='')


def download_ffmpeg():
	"""Downloads or extracts the ffmpeg executable for Windows.
	
	:return: None
	"""
	if not os.path.exists("ffmpeg.exe"):
		if not os.path.exists("ffmpeg.zip"):
			import urllib.request
			import zipfile
			print("Downloading FFMPEG. Please wait...")
			urllib.request.urlretrieve("https://raw.githubusercontent.com/rogama25/audios-on-Twitter/master/ffmpeg.zip", "ffmpeg.zip")
		zip = zipfile.ZipFile("ffmpeg.zip")
		zip.extractall()
		zip.close()
		os.remove("ffmpeg.zip")
