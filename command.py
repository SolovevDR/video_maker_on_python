import os
import video_maker_function
import derect_function

def tranclate_time(time):
    numbers = '0123456789'
    flag = False
    min = ''
    sec = ''
    for j in range(len(time)):
        if (flag == False) and (time[j] in numbers):
            min = min + time[j]
        elif (flag == True) and (time[j] in numbers):
            sec = sec + time[j]
        else:
            flag = True
    try:
        if sec == '':
            sec = 0
        times = int(min) * 60 + int(sec)
        print(times)
    except:
        times = False
    return times

def do_command_list(user_id):
    spic = extracting_commands_from_command_file(user_id)
    flag = None
    names = []
    numbers = '0123456789'
    for i in range(len(spic)):
        if spic[i][0] == '0':  # работает надеюсь больше делать ничего не буду тут
            print('0' , i)
            start = tranclate_time(spic[i][2])
            end = tranclate_time(spic[i][3])
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.cut_video(video_name, start, end, user_id)
        elif spic[i][0] == '1':
            print('1', i)
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for j in range(len(spic[i])):
                if j == 0:
                    pass
                else:
                    video_name = 'video_' + str(spic[i][j]) + '.'
                    for k in dir_files:  #
                        if video_name in k:
                            video_name = k
                            names.append(video_name)
                            break
            flag = True
            os.chdir(start_dir)
        elif spic[i][0] == '2':
            print('2', i)
            video_name = 'video_' + str(spic[i][3]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for j in dir_files:
                if video_name in j:
                    video_name = j
                    break
            image_name = 'image_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_image(user_id, start_dir)
            for j in dir_files:
                if image_name in j:
                    image_name = j
                    break
            time = tranclate_time(spic[i][2])
            video_maker_function.make_image_video(image_name, spic[i][1], user_id)
            video_maker_function.time_image_video(time, 'image_video' + str(spic[i][1]) + '.avi', spic[i][1], user_id)
            video_maker_function.connect_vid_image_vid(video_name, 'image_video' + str(spic[i][1]) + '.avi', spic[i][4],
                                                       user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '3':
            print('3', i)
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.make_video_white_black(video_name, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '4':
            print('4', i)
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.extract_audio_from_video(video_name, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '5':
            print('5', i)
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for j in dir_files:
                if video_name in j:
                    video_name = j
                    break
            video_name = os.getcwd() + '/vid/user_' + str(user_id) + '/' + video_name
            os.chdir(start_dir)

            audio_name = 'audio_' + str(spic[i][2]) + '.'
            dir_files = derect_function.checking_for_audio(user_id, start_dir)
            for j in dir_files:
                if audio_name in j:
                    audio_name = j
                    break
            audio_name = os.getcwd() + '/aud/user_' + str(user_id) + '/' + audio_name
            os.chdir(start_dir)

            print('номер ', i)
            start_aud = tranclate_time(spic[i][3])
            end_aud = tranclate_time(spic[i][4])

            start_vid = tranclate_time(spic[i][5])
            end_vid = tranclate_time(spic[i][6])

            video_maker_function.add_music_without_vid_audio(video_name, audio_name, start_aud, end_aud, start_vid,
                                                             end_vid, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '6':
            print('6', i)
            #for i in range(len(spic)):
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for j in dir_files:
                if video_name in j:
                    video_name = j
                    break
            video_name = os.getcwd() + '/vid/user_' + str(user_id) + '/' + video_name
            os.chdir(start_dir)

            audio_name = 'audio_' + str(spic[i][2]) + '.'
            dir_files = derect_function.checking_for_audio(user_id, start_dir)
            for j in dir_files:
                if audio_name in j:
                    audio_name = j
                    break
            audio_name = os.getcwd() + '/aud/user_' + str(user_id) + '/' + audio_name
            os.chdir(start_dir)

            start_aud = tranclate_time(spic[i][3])
            end_aud = tranclate_time(spic[i][4])

            start_vid = tranclate_time(spic[i][5])
            end_vid = tranclate_time(spic[i][6])

            video_maker_function.add_music_with_vid_audio(video_name, audio_name, start_aud, end_aud, start_vid,
                                                          end_vid, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '7':
            print('7', i)
            koef = float(spic[i][2])
            print(koef)
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.editing_audio_in_video(video_name, koef, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '8':
            print('8', i)
            koef = float(spic[i][2])
            print(koef)
            audio_name = 'audio_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_audio(user_id, start_dir)
            for i in dir_files:
                if audio_name in i:
                    audio_name = i
                    break
            print(audio_name)
            video_maker_function.editing_audio_in_mus(audio_name, koef, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '9':
            print('9', i)
            koef = float(spic[i][2])
            print(koef)
            start = tranclate_time(spic[i][3])
            end = tranclate_time(spic[i][4])
            video_name = 'video_' + str(spic[i][1]) + '.'
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_video(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.editing_part_audio_in_video(video_name, koef, start, end, user_id)
            os.chdir(start_dir)
        elif spic[i][0] == '10':
            print('10', i)
            start = tranclate_time(spic[i][2])
            end = tranclate_time(spic[i][3])
            print(start)
            print(end)
            start_dir = os.getcwd()
            video_name = 'audio_' + str(spic[i][1]) + '.'
            dir_files = derect_function.checking_for_audio(user_id, start_dir)
            for i in dir_files:
                if video_name in i:
                    video_name = i
                    break
            video_maker_function.cut_audio(video_name, start, end, user_id)
            os.chdir(start_dir)
            print(video_name)
    connection(user_id, names, flag)

def connection(user_id, names, flag):
    start_dir = os.getcwd()
    if flag == True:
        os.chdir(start_dir)
        video_maker_function.resize_vid(names, user_id)
        video_maker_function.connect_video(names, user_id)
        os.chdir(start_dir)
    else:
        pass

def extracting_commands_from_command_file(user_id):
    file1 = open("user_932229437.txt", "r")
    spic = []
    #засунуть в оболочку функции
    while True:
        # считываем строку
        line = file1.readline()
        time_line = line.split()
        if len(time_line) != 0:
            spic.append(time_line)
        # прерываем цикл, если строка пустая
        if not line:
            break
        # выводим строку
        #print(line.strip())

    # закрываем файл
    file1.close
    return spic

#do_command_list(user_id)

