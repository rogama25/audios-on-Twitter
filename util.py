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
	if not os.path.exists("ffmpeg.exe"):  # Check if ffmpeg was already downloaded and extracted
		import zipfile
		import urllib.request
		version = urllib.request.urlopen("https://raw.githubusercontent.com/rogama25/audiosToTwitter/master/latest-ffmpeg.txt").read() # Get the last ffmpeg version from my repo
		version = version.decode("UTF-8")
		zip_valid = False
		if os.path.exists("ffmpeg.zip"):  # Check if ffmpeg was downloaded but not extracted
			try:
				zip = zipfile.ZipFile("ffmpeg.zip")
				zip_valid = True
			except zipfile.BadZipFile:  # Corrupt zip file
				print("ffmpeg zip file detected but it's corrupt. We'll have to download it again.")
		if not zip_valid:
			import requests
			import progress.bar
			import shutil
			import sys
			char = input("Do you want to download ffmpeg now? This will download around 60MiB of data. [y/n] ")
			while True:
				if char.lower() == "n":
					sys.exit(1)
				if char.lower() == "y":
					break
				char = input("[y/n] ")
			print("Downloading FFMPEG. Please wait...")
			url = "http://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-" + version + "-win32-static.zip"
			with requests.get(url, stream=True) as r:
				r.raise_for_status()
				with open("ffmpeg.zip", 'wb') as f:
					file_size = int(r.headers["Content-Length"])
					with progress.bar.Bar("Downloading... " + str(round(file_size/1024/1024,2)) + " MiB", suffix="%(percent)d%% ETA: %(eta)ds") as progress_bar:
						for chunk in r.iter_content(chunk_size=8192):
							progress_bar.next(1/(float(file_size)/8192)*100)
							if chunk:
								f.write(chunk)
		zip = zipfile.ZipFile("ffmpeg.zip")  # Extract zip
		zip.extract("ffmpeg-"+version+"-win32-static/bin/ffmpeg.exe")
		os.rename("ffmpeg-"+version+"-win32-static/bin/ffmpeg.exe", "ffmpeg.exe")
		shutil.rmtree("ffmpeg-"+version+"-win32-static")
		zip.close()
		os.remove("ffmpeg.zip")
