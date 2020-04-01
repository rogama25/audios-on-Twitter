import os
import getpass
import platform
from languages import get_string


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
        import shutil
        version = urllib.request.urlopen(
            "https://raw.githubusercontent.com/rogama25/audiosToTwitter/master/latest-ffmpeg.txt").read()  # Get the last ffmpeg version from my repo
        version = version.decode("UTF-8")
        zip_valid = False
        if os.path.exists("ffmpeg.zip"):  # Check if ffmpeg was downloaded but not extracted
            try:
                zip = zipfile.ZipFile("ffmpeg.zip")
                zip_valid = True
            except zipfile.BadZipFile:  # Corrupt zip file
                print(get_string("ffmpeg_corrupt"))
        if not zip_valid:
            import requests
            import progress.bar
            import sys
            char = input(get_string("download_ffmpeg"))
            while True:
                if char.lower() == "n":
                    sys.exit(1)
                if char.lower() == "y":
                    break
                char = input("[y/n] ")
            print(get_string("downloading_ffmpeg"))
            url = "http://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-" + version + "-win32-static.zip"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open("ffmpeg.zip", 'wb') as f:
                    file_size = int(r.headers["Content-Length"])
                    with progress.bar.Bar("Downloading... " + str(round(file_size / 1024 / 1024, 2)) + " MiB",
                                          suffix="%(percent)d%% ETA: %(eta)ds") as progress_bar:
                        for chunk in r.iter_content(chunk_size=8192):
                            progress_bar.next(1 / (float(file_size) / 8192) * 100)
                            if chunk:
                                f.write(chunk)
        zip = zipfile.ZipFile("ffmpeg.zip")  # Extract zip
        zip.extract("ffmpeg-" + version + "-win32-static/bin/ffmpeg.exe")
        os.rename("ffmpeg-" + version + "-win32-static/bin/ffmpeg.exe", "ffmpeg.exe")
        shutil.rmtree("ffmpeg-" + version + "-win32-static")
        zip.close()
        os.remove("ffmpeg.zip")
    else:
        import urllib.request
        import subprocess
        import re
        import zipfile
        import shutil
        version = urllib.request.urlopen(
            "https://raw.githubusercontent.com/rogama25/audiosToTwitter/master/latest-ffmpeg.txt").read()  # Get the last ffmpeg version from my repo
        version = version.decode("UTF-8")
        result = subprocess.run("ffmpeg -version", capture_output=True)
        oldversion = re.search("(?<=ffmpeg version )[^ ]*", str(result.stdout))
        oldversion = oldversion.group(0)
        if version > oldversion:
            import requests
            import progress.bar
            import sys
            print(get_string("new_ffmpeg").format(oldversion, version))
            char = input(get_string("update_ffmpeg"))
            while True:
                if char.lower() == "n":
                    sys.exit(1)
                if char.lower() == "y":
                    break
                char = input("[y/n] ")
            print(get_string("downloading_ffmpeg"))
            url = "http://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-" + version + "-win32-static.zip"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open("ffmpeg.zip", 'wb') as f:
                    file_size = int(r.headers["Content-Length"])
                    with progress.bar.Bar("Downloading... " + str(round(file_size / 1024 / 1024, 2)) + " MiB",
                                          suffix="%(percent)d%% ETA: %(eta)ds") as progress_bar:
                        for chunk in r.iter_content(chunk_size=8192):
                            progress_bar.next(1 / (float(file_size) / 8192) * 100)
                            if chunk:
                                f.write(chunk)
            zip = zipfile.ZipFile("ffmpeg.zip")  # Extract zip
            zip.extract("ffmpeg-" + version + "-win32-static/bin/ffmpeg.exe")
            os.remove("ffmpeg.exe")
            os.rename("ffmpeg-" + version + "-win32-static/bin/ffmpeg.exe", "ffmpeg.exe")
            shutil.rmtree("ffmpeg-" + version + "-win32-static")
            zip.close()
            os.remove("ffmpeg.zip")


def get_version():
    return "1.7"


def get_config_dir():
    "Gets configuration folder"
    if platform.system() == "Windows":
        return os.getenv("APPDATA") + "\\rogama\\audiosToTwitter\\"
    elif platform.system() == "Darwin":
        return "~/Library/Preferences/rogama/audiosToTwitter/"
    elif platform.system() == "Linux":
        if not os.getenv("XDG_CONFIG_HOME"):
            return os.getenv("HOME") + "/.config/rogama/audiosToTwitter/"
        return os.getenv("XDG_CONFIG_HOME") + "/rogama/audiosToTwitter/"


def get_lang_dir():
    return "./lang"
