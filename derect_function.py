import os
import time

#создание директории видео под пользователя
def creat_vid_dir(user_id):
     if not os.path.isdir('vid/user_' + str(user_id)):
          os.mkdir('vid/user_' + str(user_id))

#создание директории аудио под пользователя
def creat_aud_dir(user_id):
     if not os.path.isdir('aud/user_' + str(user_id)):
          os.mkdir('aud/user_' + str(user_id))

#создание директории изображений под пользователя
def creat_img_dir(user_id):
     if not os.path.isdir('img/user_' + str(user_id)):
          os.mkdir('img/user_' + str(user_id))

#создание директории команды под пользователя
def creat_com_dir(user_id):
     if not os.path.isdir('com/user_' + str(user_id)):
          os.mkdir('com/user_' + str(user_id))

#создание результирующей директории под пользователя
def creat_res_dir(user_id):
     if not os.path.isdir('res/user_' + str(user_id)):
          os.mkdir('res/user_' + str(user_id))

#переименовать видео файл в директоории
def rename_vidfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     flag = False
     format = ''
     dir_files = os.listdir()
     for j in range(len(old_name)):
          if old_name[j] == '.':
               flag = True
          if flag == True:
               format = format + old_name[j]
     if 'video_res' in dir_files:
          os.rename(old_name, 'video_' + str(len(dir_files)-1) + str(format))
     else:
          os.rename(old_name, 'video_' + str(len(dir_files)) + str(format))
     os.chdir(start_dir)

#переименовать аудио файл в директоории
def rename_audfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
     flag = False
     format = ''
     dir_files = os.listdir()
     for j in range(len(old_name)):
          if old_name[j] == '.':
               flag = True
          if flag == True:
               format = format + old_name[j]
     if 'audio_res' in dir_files:
          os.rename(old_name, 'audio_' + str(len(dir_files)-1) + str(format))
     else:
          os.rename(old_name, 'audio_' + str(len(dir_files))+ str(format))
     os.chdir(start_dir)

#переименовать изображения в директоории
def rename_imgfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
     flag = False
     format = ''
     dir_files = os.listdir()
     for j in range(len(old_name)):
          if old_name[j] == '.':
               flag = True
          if flag == True:
               format = format + old_name[j]
     if 'photo_res' in dir_files:
          os.rename(old_name, 'photo_' + str(len(dir_files)-1) + str(format))
     else:
          os.rename(old_name, 'photo_' + str(len(dir_files)) + str(format))
     os.chdir(start_dir)

def creat_command_file(user_id):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/com/user_' + str(user_id) + '/')
     f = open('user_' + str(user_id) + '.txt', 'w')
     f.close()
     os.chdir(start_dir)

def write_command_in_comad_file(user_id, command, flag):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/com/user_' + str(user_id) + '/')
     f = open('user_' + str(user_id) + '.txt', 'a')
     f.write(command)
     if flag == True:
          f.write('\n')
     else:
          f.write(' ')
     f.close()
     os.chdir(start_dir)

def checking_for_video_availability(user_id, start_dir):
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return len(dir_files)

def checking_for_video(user_id, start_dir):
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return dir_files

def checking_for_audio_availability(user_id, start_dir):
     os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return len(dir_files)

def checking_for_audio(user_id, start_dir):
     os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return dir_files

def checking_for_image_availability(user_id, start_dir):
     os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return len(dir_files)

def checking_for_image(user_id, start_dir):
     os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return dir_files

def checking_for_resalt(user_id, start_dir):
     os.chdir(os.getcwd() + '/res/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     os.chdir(start_dir)
     return dir_files

def take_name(file_name):
     name = ''
     for i in range(len(file_name)):
          if file_name[i] != '.':
               name = name + file_name[i]
          else:
               break
     return name

def delete_file_in_vid_dir(user_id):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     if len(dir_files) != 0:
          for i in range(len(dir_files)):
               os.remove(dir_files[i])
     os.chdir(start_dir)

def delete_file_in_aud_dir(user_id):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     if len(dir_files) != 0:
          for i in range(len(dir_files)):
               os.remove(dir_files[i])
     os.chdir(start_dir)

def delete_file_in_img_dir(user_id):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     if len(dir_files) != 0:
          for i in range(len(dir_files)):
               os.remove(dir_files[i])
     os.chdir(start_dir)

def delete_file_in_res_dir(user_id):
     start_dir = os.getcwd()
     os.chdir(os.getcwd() + '/res/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     if len(dir_files) != 0:
          for i in range(len(dir_files)):
               os.remove(dir_files[i])
     os.chdir(start_dir)


#os.remove('video_res_3.mp4')
'''
#просмотр пути текущей директории
print("Текущая деректория:", os.getcwd())

#создание паки в случае ее отсутсвия
if not os.path.isdir("folder"):
     os.mkdir("folder")


#изменяет текующую директирию
#os.chdir("folder")

#Удаление папки
os.rmdir("folder")
'''


#print(os.getcwd())