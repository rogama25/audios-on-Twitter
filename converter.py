import os
import ffmpy
from languages import get_string


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
        print(get_string("downloading_background"))
        urllib.request.urlretrieve("https://raw.githubusercontent.com/rogama25/audios-on-Twitter/master/media/img.png", "media/img.png")
    if duration > 140:
        duration = 140
    ff = ffmpy.FFmpeg(
        inputs={'media/img.png': None, input_file + '.ogg': None},
        outputs={input_file + '.mp4': '-c:v libx264 -c:a aac -tune stillimage -pix_fmt yuv420p -t ' + str(duration)},
        global_options="-y -loglevel 0 -loop 1"
    )
    ff.run()
