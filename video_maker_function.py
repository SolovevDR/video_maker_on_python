from moviepy.editor import *
from PIL import Image
import cv2

#обрезает видео по заданному времени и сохраняет его(работает правильно)
def cut_video(start_time, end_time, name_video):
    vid = VideoFileClip(name_video)
    trim_vid = vid.subclip(start_time, end_time)
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#склеивает все видео в единый видеоряд(работает правильно)
def connect_video(name_video1, name_videos2):
    vid_1 = VideoFileClip(name_video1)
    vid_2 = VideoFileClip(name_videos2)
    if vid_1.size != vid_2.size:
        if vid_1.size[0] > vid_1.size[1]:
            if (vid_1.size[0] != 1920) and (vid_1.size[1] != 1080):
                vid_1 = vid_1.resize((1920, 1080))
            if (vid_2.size[0] != 1920) and (vid_2.size[1] != 1080):
                vid_2 = vid_2.resize((1920, 1080))
            print('выполненно 1')
            print(vid_1.size)
            print(vid_2.size)
        else:
            if (vid_1.size[0] != 1080) and (vid_1.size[1] != 1920):
                vid_1 = vid_1.resize((1080, 1920))
            if (vid_2.size[0] != 1080) and (vid_2.size[1] != 1920):
                vid_2 = vid_2.resize((1080, 1920))
            print('выполненно 2')
            print(vid_1.size)
            print(vid_2.size)
    trim_vid = concatenate_videoclips([vid_1, vid_2])
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#создание из картинки одно секундного видео(работает правильно)
def make_image_video(name_image):
    mean_width = 0
    mean_height = 0

    im = Image.open(name_image)  # загрузка изображения
    width, height = im.size
    mean_width += width  # подсчет средней
    mean_height += height  # высоты и ширины

    frame = cv2.imread(name_image)

    height, width, layers = frame.shape
    video = cv2.VideoWriter('image_video.avi', 0, 1, (width, height))
    video.write(cv2.imread(name_image))

#задание продолжительности видео из картинки(работает правильно)
def time_image_video(sec_vid_image, name_image):
    vid_image = VideoFileClip(name_image)
    list_vid = []
    for i in range(sec_vid_image):
        list_vid.append(vid_image)

    trim_vid = concatenate_videoclips(list_vid)
    trim_vid.write_videofile('video_image.avi', codec='libx264')

#соеденение видео и картинки(работает правильно)
def connect_vid_image_vid(key, name_video1, name_video2):
    vid = VideoFileClip(name_video1)
    vid_image = VideoFileClip(name_video2)
    vid = vid.resize((1920, 1080))
    vid_image = vid_image.resize((1920, 1080))
    # если ключ равен 1, то сначало будет сделано добавлено видео
    if key == 1:
        trim_vid = concatenate_videoclips([vid, vid_image])
    else:
        trim_vid = concatenate_videoclips([vid_image, vid])
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#наложение музыки на указанный интервал, но полностью уберет звук, с части где будет наложена музыка(работает правильно)
def add_music_without_vid_audio(name_video, mus, start_time_mus, end_time_mus):
    vid = VideoFileClip(name_video)
    vid_before_mus = vid.subclip(0, start_time_mus-0.01)
    vid_after_mus = vid.subclip(end_time_mus+0.01, vid.duration)
    vid_with_mus = vid.subclip(start_time_mus, end_time_mus)
    clip = mus.subclip(start_time_mus, end_time_mus)
    vid_with_mus = vid_with_mus.set_audio(clip)
    trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#наложение музыки на указанный интервал, с музыкой смешанной с аудио из видео(работает правильно)
def add_music_with_vid_audio(name_video, name_music, start_time_mus, end_time_mus):
    vid = VideoFileClip(name_video)
    mus = AudioFileClip(name_music)
    vid_before_mus = vid.subclip(0, start_time_mus - 0.01)
    vid_after_mus = vid.subclip(end_time_mus + 0.01, vid.duration)
    vid_with_mus = vid.subclip(start_time_mus, end_time_mus)
    mus = mus.subclip(start_time_mus, end_time_mus)
    new_audioclip = CompositeAudioClip([vid_with_mus.audio, mus])
    vid_with_mus.audio = new_audioclip
    trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#редактирование громкости аудио(работает правильно)
def editing_audio_in_mus(name_music, koef):
    mus = AudioFileClip(name_music)
    mus = mus.volumex(koef)
    mus.write_audiofile('music_2.mp3')

#редактирование громкости видео(работает правильно)
def editing_audio_in_video(name_video, koef):
    vid = VideoFileClip(name_video)
    vid = vid.volumex(koef)
    vid.write_videofile('video_res_2.mp4', codec='libx264')

#редактирование громкости видео в заданном интеревале (работает правильно)
def editing_part_audio_in_video(name_video, start_time, end_time, koef):
    vid = VideoFileClip(name_video)
    vid_before_mus = vid.subclip(0, start_time-0.01)
    vid_after_mus = vid.subclip(end_time+0.01, vid.duration)
    vid_with_mus = vid.subclip(start_time, end_time)
    print('с музыкой измененный: ', vid_with_mus.duration)
    print('начало видео: ', vid_before_mus.duration)
    print('конец видео: ', vid_after_mus.duration)

    vid_with_mus = vid_with_mus.volumex(koef)
    trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    print('все видео длительность: ', trim_vid.duration)
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#конвертирование видео в чб(работает правильно)
def make_video_white_black(name_video):
    vid = VideoFileClip(name_video)
    trim_vid = vid.fx(vfx.blackwhite)
    trim_vid.write_videofile('video_res.mp4', codec='libx264')

#обрезает аудио файл(работает правильно)
def cut_audio(name_music, start_time,end_time):
    mus = AudioFileClip(name_music)
    mus = mus.subclip(start_time, end_time)
    mus.write_audiofile('cut_mus.mp3')

#извлечение аудио из видео(работает правильно)
def extract_audio_from_video(name_video):
    audioclip = AudioFileClip(name_video)
    audioclip.write_audiofile("out_audio.mp3")

#добавление текста(пишу)
def add_text(name_video, text_for_video,text_start_time, text_end_time, size, color):
    #параметры для указания позиции расположения текста
    #(пока так будет работать, возможно сделаю формулу для расчета позиции на видео)
    # right, center, left
    # top, center, bottom
    vid = VideoFileClip(name_video)
    text1 = TextClip(text_for_video,  fontsize=size, font='Courier', color=color)
    txt_clip = text1.set_pos(("right", "top"), relative=True).set_duration(text_end_time-text_start_time)
    text2 = TextClip(text_for_video, fontsize=size, font='TimesNewRoman', color=color)
    txt_clip_2 = text2.set_pos(("right", "top"), relative=True).set_duration(5)
    video = CompositeVideoClip([vid, txt_clip.set_start(text_start_time), txt_clip_2.set_start(10)])
    video.write_videofile('video_res.mp4', codec='libx264')







#vid = VideoFileClip('video.mp4')
#mus = AudioFileClip('music.mp3')
print('Введите время в секндах')

#start_time = float(input('Старт'))
#end_time = float(input('Конец'))

#add_text('video.mp4', 'test video', 0, 10 ,100, 'white')
#make_video_white_black('video.mp4')
#extract_audio_from_video('video.mp4')
#cut_audio('music.mp3', 25, 47)
#editing_part_audio_in_video('video.mp4', 3, 15, 0)
#make_image_video()
#connect_video('video.mp4', 'video_vert.mp4')
#connect_vid_image_vid(0)
#time_image_video(5)
#connect_image(5)
#editing_audio_in_video(vid, 2)
#editing_audio_in_mus(mus, 0.5)
#add_music_with_vid_audio('video.mp4', 'music.mp3', 1, 25)
#add_music_without_vid_audio(vid, mus, 1, 25)
#connect_video(videos,vid)
#list_video(videos, vid)
#cut_video(start_time_1, end_time_1, vid)
