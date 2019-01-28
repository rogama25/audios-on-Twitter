import os
import getpass


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
	getpass.getpass(prompt='')


def download_ffmpeg():
	if not os.path.exists("ffmpeg.exe"):
		import urllib.request.urlretrieve
		import zipfile
		print("Downloading FFMPEG. Please wait...")
		urllib.request.urlretrieve("https://raw.githubusercontent.com/rogama25/audios-on-Twitter/master/ffmpeg.zip", "ffmpeg.zip")
		zip = zipfile.ZipFile("ffmpeg.zip")
		zip.extractall()
