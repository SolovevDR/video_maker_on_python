import os
import time

#создание директории под пользователя
def creat_dir(user_id):
     if not os.path.isdir('vid/user_' + str(user_id)):
          os.mkdir('vid/user_' + str(user_id))

#удаление директории
def delete_dir(user_id):
     os.rmdir('vid/user_' + str(user_id))

#переименовать файл в директоории
def rename_file(user_id, old_name, start_dir):
     os.chdir(os.getcwd() + '/vid/user_' + str(user_id) + '/')
     dir_files = os.listdir()
     #print(dir_files)
     if 'video_res' in dir_files:
          os.rename(old_name, 'video_' + str(len(dir_files)-1))
     else:
          os.rename(old_name, 'video_' + str(len(dir_files)))
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