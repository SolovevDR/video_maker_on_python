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

#удаление директории
def delete_dir(user_id):
     os.rmdir('vid/user_' + str(user_id))

#переименовать видео файл в директоории
def rename_vidfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     #print(dir_files)
     if 'video_res' in dir_files:
          os.rename(old_name, 'video_' + str(len(dir_files)-1))
     else:
          os.rename(old_name, 'video_' + str(len(dir_files)))
     os.chdir(start_dir)

#переименовать аудио файл в директоории
def rename_audfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/aud/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     #print(dir_files)
     if 'audio_res' in dir_files:
          os.rename(old_name, 'audio_' + str(len(dir_files)-1))
     else:
          os.rename(old_name, 'audio_' + str(len(dir_files)))
     os.chdir(start_dir)

#переименовать изображения в директоории
def rename_imgfile(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/img/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     #print(dir_files)
     if 'photo_res' in dir_files:
          os.rename(old_name, 'photo_' + str(len(dir_files)-1))
     else:
          os.rename(old_name, 'photo_' + str(len(dir_files)))
     os.chdir(start_dir)




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


print(os.getcwd())