from PIL import Image
import os
import ffmpy


def convert(input_file: str, duration: float):
	if not os.path.exists("media/img.png"):
		img = Image.new("RGB", (240, 240))
		img.save("media/img.png")
	ff = ffmpy.FFmpeg(
		inputs={'media/img.png': None, input_file + '.ogg': None},
		outputs={input_file + '.mp4': '-c:v libx264 -c:a aac -tune stillimage -pix_fmt yuv420p -vf tpad=stop_mode=clone:stop_duration=' + str(duration)},
		global_options="-loglevel 0"
	)
	ff.run()
#"-framerate 1/" + str(duration)