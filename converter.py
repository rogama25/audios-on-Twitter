from PIL import Image
import os
import moviepy.editor as moviepy


def convert(input_file:str, duration:float):
	if not os.path.exists("media/img.png"):
		img = Image.new("RGB",(240,240))
		img.save("media/img.png")
	video = moviepy.ImageClip("media/img.png")
	video = video.set_duration(duration)
	audio = moviepy.AudioFileClip(input_file+".ogg")
	video = video.set_audio(audio)
	video.write_videofile(input_file+".mp4",fps=30, audio_codec="aac")
