import ffmpeg

input = ffmpeg.input('video.mp4')
audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
video = input.video.hflip()
output = ffmpeg.output(audio, video, 'out.mp4')
ffmpeg.overwrite_output(output)
