from moviepy.editor import *
import derect_function
from PIL import Image
import cv2

#обрезает видео по заданному времени и сохраняет его(работает правильно)
def cut_video(name_video, start_time, end_time, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    vid = VideoFileClip(name_video)
    if start_time > vid.duration:
        start_time = 0
    if end_time > vid.duration:
        end_time = vid.duration
    if end_time > start_time:
        trim_vid = vid.subclip(start_time, end_time)
    elif start_time == end_time:
        trim_vid = vid.subclip(0, vid.duration)
    else:
        trim_vid = vid.subclip(end_time, start_time)
    old_name_video = derect_function.take_name(name_video)
    trim_vid.write_videofile('res_' + str(old_name_video) +'.mp4', codec='libx264')
    vid.close()
    os.remove(name_video)
    os.rename('res_' + str(old_name_video) + '.mp4', name_video)
    os.chdir(start_dir)

#создание из картинки одно секундного видео(работает правильно)
def make_image_video(name_image, number, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
    mean_width = 0
    mean_height = 0

    im = Image.open(name_image)  # загрузка изображения
    width, height = im.size
    mean_width += width  # подсчет средней
    mean_height += height  # высоты и ширины

    frame = cv2.imread(name_image)

    height, width, layers = frame.shape
    video = cv2.VideoWriter('image_video' + str(number) + '.avi', 0, 1, (width, height))
    video.write(cv2.imread(name_image))
    os.chdir(start_dir)

#задание продолжительности видео из картинки(работает правильно)
def time_image_video(sec_vid_image, name_image, number, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
    vid_image = VideoFileClip(name_image)
    list_vid = []
    for i in range(sec_vid_image):
        list_vid.append(vid_image)

    trim_vid = concatenate_videoclips(list_vid)
    trim_vid.write_videofile('image_video' + str(number) + '.avi', codec='libx264')

    os.chdir(start_dir)

#соеденение видео и картинки(работает правильно)
def connect_vid_image_vid(name_video1, name_video2, key, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    vid = VideoFileClip(name_video1)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
    vid_image = VideoFileClip(name_video2)
    vid_image = vid_image.resize((vid.size[0], vid.size[1]))
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    old_name_video = derect_function.take_name(name_video1)
    # если ключ равен 1, то сначало будет сделано добавлено видео
    if key == 1:
        trim_vid = concatenate_videoclips([vid, vid_image])
    else:
        trim_vid = concatenate_videoclips([vid_image, vid])
    trim_vid.write_videofile('res_' + str(old_name_video) +'.mp4', codec='libx264')
    vid.close()
    vid_image.close()

    os.remove(name_video1)
    os.rename('res_' + str(old_name_video) + '.mp4', name_video1)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
    os.remove(name_video2)

#наложение музыки на указанный интервал, но полностью уберет звук, с части где будет наложена музыка(работает правильно)
def add_music_without_vid_audio(name_video, name_music, start_audiotime, end_audiotime, start_videotime, end_videotime, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
    mus = AudioFileClip(name_music)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    vid = VideoFileClip(name_video)

    old_name_video = derect_function.take_name(name_video)

    if start_audiotime >= end_audiotime:
        a = start_audiotime
        start_audiotime = end_audiotime
        end_audiotime = a
    elif start_audiotime == end_audiotime:
        start_audiotime = 0
        end_audiotime = mus.duration

    if start_videotime >= end_videotime:
        a = start_videotime
        start_videotime = end_videotime
        end_videotime = a
    elif start_videotime == end_videotime:
        start_videotime = 0
        end_videotime = mus.duration

    if start_audiotime > mus.duration:
        start_audiotime = 0

    if start_videotime > vid.duration:
        start_videotime = 0

    if end_audiotime > mus.duration:
        end_audiotime = mus.duration

    if end_videotime > vid.duration:
        end_videotime = vid.duration

    if end_videotime - start_videotime > end_audiotime - start_audiotime:
        end_videotime = start_audiotime + (end_videotime - start_videotime)
    elif end_videotime - start_videotime < end_audiotime - start_audiotime:
        end_audiotime = start_audiotime + (end_videotime - start_videotime)

    if end_audiotime > mus.duration:
        end_audiotime = mus.duration

    if end_videotime > mus.duration:
        end_videotime = vid.duration



    clip = mus.subclip(start_audiotime, end_videotime)
    vid_before_mus = vid.subclip(0, start_videotime)
    vid_after_mus = vid.subclip(end_videotime, vid.duration)
    vid_with_mus = vid.subclip(start_videotime, end_videotime)
    vid_with_mus = vid_with_mus.set_audio(clip)
    if start_videotime != 0:
        trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    else:
        trim_vid = concatenate_videoclips([vid_with_mus, vid_after_mus])
    trim_vid.write_videofile('res' + '.mp4', codec='libx264')

    vid.close()
    mus.close()
    vid_with_mus.close()
    vid_before_mus.close()
    vid_after_mus.close()
    os.remove(name_video)
    os.rename('res' + '.mp4', name_video)
    os.chdir(start_dir)

#наложение музыки на указанный интервал, с музыкой смешанной с аудио из видео(работает правильно)
def add_music_with_vid_audio(name_video, name_music, start_audiotime, end_audiotime, start_videotime, end_videotime, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
    mus = AudioFileClip(name_music)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    vid = VideoFileClip(name_video)

    old_name_video = derect_function.take_name(name_video)

    if start_audiotime >= end_audiotime:
        a = start_audiotime
        start_audiotime = end_audiotime
        end_audiotime = a
    elif start_audiotime == end_audiotime:
        start_audiotime = 0
        end_audiotime = mus.duration

    if start_videotime >= end_videotime:
        a = start_videotime
        start_videotime = end_videotime
        end_videotime = a
    elif start_videotime == end_videotime:
        start_videotime = 0
        end_videotime = mus.duration

    if start_audiotime > mus.duration:
        start_audiotime = 0

    if start_videotime > vid.duration:
        start_videotime = 0

    if end_audiotime > mus.duration:
        end_audiotime = mus.duration

    if end_videotime > vid.duration:
        end_videotime = vid.duration

    if end_videotime - start_videotime > end_audiotime - start_audiotime:
        end_videotime = start_audiotime + (end_videotime - start_videotime)
    elif end_videotime - start_videotime < end_audiotime - start_audiotime:
        end_audiotime = start_audiotime + (end_videotime - start_videotime)

    if end_audiotime > mus.duration:
        end_audiotime = mus.duration

    if end_videotime > mus.duration:
        end_videotime = vid.duration

    vid_before_mus = vid.subclip(0, start_videotime)

    vid_after_mus = vid.subclip(end_videotime , vid.duration)

    vid_with_mus = vid.subclip(start_videotime, end_videotime)
    clip = mus.subclip(start_audiotime, end_audiotime)
    new_audioclip = CompositeAudioClip([vid_with_mus.audio, clip])
    vid_with_mus.audio = new_audioclip
    if start_videotime != 0:
        trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    else:
        trim_vid = concatenate_videoclips([vid_with_mus, vid_after_mus])
    trim_vid.write_videofile('res' + '.mp4', codec='libx264')

    vid.close()
    mus.close()
    vid_with_mus.close()
    vid_before_mus.close()
    vid_after_mus.close()
    os.remove(name_video)
    os.rename('res' + '.mp4', name_video)
    os.chdir(start_dir)

#редактирование громкости аудио(работает правильно)(доделать сохранение файла)
def editing_audio_in_mus(name_music, koef, user_id):
    start_dir = os.getcwd()
    print(os.getcwd())
    os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
    print(os.getcwd())
    print(name_music)
    mus = AudioFileClip(name_music)
    old_name_audio = derect_function.take_name(name_music)
    mus = mus.volumex(koef)
    mus.write_audiofile('res_' + str(old_name_audio) +'.mp3')
    mus.close()
    os.remove(name_music)
    os.rename('res_' + str(old_name_audio) + '.mp3', name_music)
    os.chdir(start_dir)

#редактирование громкости видео(работает правильно)
def editing_audio_in_video(name_video, koef, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')

    vid = VideoFileClip(name_video)
    vid = vid.volumex(koef)
    old_name_video = derect_function.take_name(name_video)
    vid.write_videofile('res_' + str(old_name_video) +'.mp4', codec='libx264')
    vid.close()
    os.remove(name_video)
    os.rename('res_' + str(old_name_video) + '.mp4', name_video)
    os.chdir(start_dir)

#редактирование громкости видео в заданном интеревале (работает правильно)
def editing_part_audio_in_video(name_video, koef, start_time, end_time, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')

    vid = VideoFileClip(name_video)
    if start_time > vid.duration:
        start_time = 0
    if end_time > vid.duration:
        end_time = vid.duration
    vid_before_mus = vid.subclip(0, start_time)
    vid_after_mus = vid.subclip(end_time, vid.duration)
    vid_with_mus = vid.subclip(start_time, end_time)
    vid_with_mus = vid_with_mus.volumex(koef)
    old_name_video = derect_function.take_name(name_video)
    if end_time > start_time:
        trim_vid = vid.subclip(start_time, end_time)
    elif start_time == end_time:
        trim_vid = vid.subclip(0, vid.duration)
    else:
        trim_vid = vid.subclip(end_time, start_time)

    trim_vid = concatenate_videoclips([vid_before_mus, vid_with_mus, vid_after_mus])
    print('все видео длительность: ', trim_vid.duration)
    trim_vid.write_videofile('res_' + str(old_name_video) +'.mp4', codec='libx264')
    vid.close()
    vid_before_mus.close()
    vid_after_mus.close()
    vid_with_mus.close()
    os.remove(name_video)
    os.rename('res_' + str(old_name_video) + '.mp4', name_video)
    os.chdir(start_dir)

#конвертирование видео в чб(работает правильно)
def make_video_white_black(name_video, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    old_name_video = derect_function.take_name(name_video)
    vid = VideoFileClip(name_video)
    trim_vid = vid.fx(vfx.blackwhite)
    trim_vid.write_videofile('res_' + str(old_name_video) +'.mp4', codec='libx264')
    vid.close()
    os.remove(name_video)
    os.rename('res_' + str(old_name_video) + '.mp4', name_video)
    os.chdir(start_dir)

#обрезает аудио файл(работает правильно)
def cut_audio(name_music, start_time,end_time, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
    mus = AudioFileClip(name_music)
    old_name_audio = derect_function.take_name(name_music)
    if start_time > mus.duration:
        start_time = 0
    if end_time > mus.duration:
        end_time = mus.duration
    if end_time > start_time:
        trim_mus = mus.subclip(start_time, end_time)
    elif start_time == end_time:
        trim_mus = mus.subclip(0, mus.duration)
    else:
        trim_mus = mus.subclip(end_time, start_time)
    trim_mus.write_audiofile('res_' + str(old_name_audio) +'.mp3')
    mus.close()
    os.remove(name_music)
    os.rename('res_' + str(old_name_audio) + '.mp3', name_music)
    os.chdir(start_dir)

#извлечение аудио из видео(работает правильно)
def extract_audio_from_video(name_video, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    old_name_audio = derect_function.take_name(name_video)
    audioclip = AudioFileClip(name_video)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/res/user_' + str(user_id) + '/')
    audioclip.write_audiofile("out_audio" + str(old_name_audio) +".mp3")
    audioclip.close()
    os.chdir(start_dir)


#добавление текста(не будет в первой версии сайта и бота) !!!!не трогаем
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

#создает фон для склеивания видео(работает правильно)
def resize_vid(vid_names, user_id):
    start_dir = os.getcwd()
    max_width_vert_vid = 0
    max_height_vert_vid = 0
    max_height_gor_vid = 0
    max_width_gor_vid = 0
    sum_vert = 0
    sum_gor = 0
    time_len = 0

    os.chdir(os.getcwd() + '/working_materials/')

    black_vid = VideoFileClip('black_video.avi')
    print(black_vid.size)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    for i in vid_names:
        vid = VideoFileClip(i)
        time_len = time_len + vid.duration
        if vid.size[0] >= vid.size[1]:
            sum_gor = sum_gor + 1
            if max_width_gor_vid < vid.size[0]:
               max_width_gor_vid = vid.size[0]
            if max_height_gor_vid < vid.size[1]:
               max_height_gor_vid = vid.size[1]
        elif vid.size[0] < vid.size[1]:
            sum_vert = sum_vert + 1
            if max_width_vert_vid < vid.size[0]:
               max_width_vert_vid = vid.size[0]
            if max_height_vert_vid < vid.size[1]:
               max_height_vert_vid = vid.size[1]
    if sum_gor >= sum_vert:
        black_vid = black_vid.resize((max_width_gor_vid, max_height_gor_vid))
    else:
        black_vid = black_vid.resize((max_width_vert_vid, max_height_vert_vid))
    print(black_vid.size)

    list_vid = []
    print(int(time_len))
    for i in range(int(time_len)+1):
        list_vid.append(black_vid)

    trim_vid = concatenate_videoclips(list_vid)
    trim_vid.write_videofile('resize_black_video.avi', codec='libx264')
    os.chdir(start_dir)

#склеивает видео(работает правильно)
def connect_video(vid_names, user_id):
    start_dir = os.getcwd()
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    blacl_vid = VideoFileClip('resize_black_video.avi')
    list_vid = [blacl_vid]
    len_vid =[0]
    sum_len = 0
    for i in vid_names:
        vid = VideoFileClip(i)
        if vid.size[0] > vid.size[1]:
            vid = vid.resize(width = blacl_vid.size[0])
        else:
            vid = vid.resize(height = blacl_vid.size[1])
        list_vid.append(vid)
        sum_len = sum_len + vid.duration
        len_vid.append(sum_len)
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/res/user_' + str(user_id) + '/')
    print(len_vid)
    if  len(vid_names) == 1:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0])])
    elif len(vid_names) == 2:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1])])
    elif len(vid_names) == 3:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2])])
    elif len(vid_names) == 4:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3])])
    elif len(vid_names) == 5:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4])])
    elif len(vid_names) == 6:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5])])
    elif len(vid_names) == 7:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6])])
    elif len(vid_names) == 8:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7])])
    elif len(vid_names) == 9:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8])])
    elif len(vid_names) == 10:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9])])
    elif len(vid_names) == 11:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10])])
    elif len(vid_names) == 12:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11])])
    elif len(vid_names) == 13:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12])])
    elif len(vid_names) == 14:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13])])
    elif len(vid_names) == 15:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14])])
    elif len(vid_names) == 16:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15])])
    elif len(vid_names) == 17:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15]),
             list_vid[17].set_position(('center', 'center')).set_start(len_vid[16])])
    elif len(vid_names) == 18:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15]),
             list_vid[17].set_position(('center', 'center')).set_start(len_vid[16]),
             list_vid[18].set_position(('center', 'center')).set_start(len_vid[17])])
    elif len(vid_names) == 19:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15]),
             list_vid[17].set_position(('center', 'center')).set_start(len_vid[16]),
             list_vid[18].set_position(('center', 'center')).set_start(len_vid[17]),
             list_vid[19].set_position(('center', 'center')).set_start(len_vid[18])])
    elif len(vid_names) == 20:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15]),
             list_vid[17].set_position(('center', 'center')).set_start(len_vid[16]),
             list_vid[18].set_position(('center', 'center')).set_start(len_vid[17]),
             list_vid[19].set_position(('center', 'center')).set_start(len_vid[18]),
             list_vid[20].set_position(('center', 'center')).set_start(len_vid[19])])
    elif len(vid_names) == 21:
        trim_vid = CompositeVideoClip(
            [list_vid[0], list_vid[1].set_position(('center', 'center')).set_start(len_vid[0]),
             list_vid[2].set_position(('center', 'center')).set_start(len_vid[1]),
             list_vid[3].set_position(('center', 'center')).set_start(len_vid[2]),
             list_vid[4].set_position(('center', 'center')).set_start(len_vid[3]),
             list_vid[5].set_position(('center', 'center')).set_start(len_vid[4]),
             list_vid[6].set_position(('center', 'center')).set_start(len_vid[5]),
             list_vid[7].set_position(('center', 'center')).set_start(len_vid[6]),
             list_vid[8].set_position(('center', 'center')).set_start(len_vid[7]),
             list_vid[9].set_position(('center', 'center')).set_start(len_vid[8]),
             list_vid[10].set_position(('center', 'center')).set_start(len_vid[9]),
             list_vid[11].set_position(('center', 'center')).set_start(len_vid[10]),
             list_vid[12].set_position(('center', 'center')).set_start(len_vid[11]),
             list_vid[13].set_position(('center', 'center')).set_start(len_vid[12]),
             list_vid[14].set_position(('center', 'center')).set_start(len_vid[13]),
             list_vid[15].set_position(('center', 'center')).set_start(len_vid[14]),
             list_vid[16].set_position(('center', 'center')).set_start(len_vid[15]),
             list_vid[17].set_position(('center', 'center')).set_start(len_vid[16]),
             list_vid[18].set_position(('center', 'center')).set_start(len_vid[17]),
             list_vid[19].set_position(('center', 'center')).set_start(len_vid[18]),
             list_vid[20].set_position(('center', 'center')).set_start(len_vid[19]),
             list_vid[21].set_position(('center', 'center')).set_start(len_vid[20])])
    trim_vid.write_videofile('resalt_video.mp4', codec='libx264')
    for i in vid_names:
        i.close()
    blacl_vid.close()
    os.chdir(start_dir)
    os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
    os.remove('resize_black_video.avi')





#resize_vid(lis)
#connect_video_2(lis)
   # start_dir = os.getcwd()
   # os.chdir(os.getcwd() + '/working_materials/')
   # mean_width = 0
   # mean_height = 0
   #
   # im = Image.open('black.jpg')  # загрузка изображения
   # width, height = im.size
   #
   # mean_width += width  # подсчет средней
   # mean_height += height  # высоты и ширины
   #
   # frame = cv2.imread('black.jpg')
   #
   # height, width, layers = frame.shape
   # video = cv2.VideoWriter('black_video.avi', 0, 1, (width, height))
   # video.write(cv2.imread('black.jpg'))
   # os.chdir(start_dir)

#vid = VideoFileClip('video.mp4')
#mus = AudioFileClip('music.mp3')
#print('Введите время в секндах')

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
#add_music_with_vid_audio('video.mp4', 'music.mp3', 60, 400, 60)
#add_music_with_vid_audio('video.mp4', 'music.mp3', 20, 400, 0, 40)
#add_music_without_vid_audio(vid, mus, 1, 25)
#connect_video(videos,vid)
#list_video(videos, vid)
#cut_video(start_time_1, end_time_1, vid)
