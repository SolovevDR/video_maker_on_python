import telebot
from telebot import types
import os
import derect_function
import database

bot = telebot.TeleBot('1555796929:AAHtJl5ELHE9jT6OUTXSUSEjRLKe1WIzmSk')

@bot.message_handler(commands=['start'])
def start(message):

    # keyboard
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать")
    markup1.add(item1)

    bot.send_message(message.chat.id, "Это очередная хуйня, которая наверняка будет опять не закончена", reply_markup=markup1)
    database.registration_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    derect_function.creat_vid_dir(message.from_user.id)
    derect_function.creat_aud_dir(message.from_user.id)
    derect_function.creat_img_dir(message.from_user.id)



'''
@bot.message_handler(commands=['menu'])
def menu(message):

    # keyboard
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сохранить")
    item2 = types.KeyboardButton("Вернуться к последнему действию")
    markup1.add(item1).add(item2)

    bot.send_message(message.chat.id,'МЕНЮ', reply_markup=markup1)
'''



@bot.message_handler(content_types=['text'])
def action_0(message):
    if message.chat.type == 'private':
        if message.text == 'Начать': #and prov.back() == "0":

            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton("ну вроду работает")
            markup1.add(item1)

            bot.send_message(message.chat.id, "начинаем ебаться с телегой", reply_markup=markup1)
            #derect_function.creat_dir(message.chat.id)

            #bot.register_next_step_handler(message, actiom_1)
        else:

            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("ты даже тут облажался")
            markup1.add(item1)

            bot.send_message(message.chat.id, 'Ты ввел какую то хуйню',reply_markup=markup1)


@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        start_dir = os.getcwd()
        src = os.getcwd() + '/vid/user_'+ str(message.chat.id) + '/' + message.video.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            #os.chdir('/home/danila/video/video_maker_on_python/vid/user_' + str(message.chat.id) + '/') не убирать на случай если что-то в функции опять сломается
            print(os.getcwd())
            derect_function.rename_vidfile(message.chat.id, message.video.file_name, start_dir)


        bot.reply_to(message, "Видео сохранено")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['audio'])
def handle_docs_audio(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        start_dir = os.getcwd()
        src = os.getcwd() + '/aud/user_'+ str(message.chat.id) + '/' + message.audio.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            #os.chdir('/home/danila/video/video_maker_on_python/vid/user_' + str(message.chat.id) + '/') не убирать на случай если что-то в функции опять сломается
            print(os.getcwd())
            derect_function.rename_audfile(message.chat.id, message.audio.file_name, start_dir)


        bot.reply_to(message, "Аудио сохранено")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        start_dir = os.getcwd()
        src = os.getcwd() + '/img/user_'+ str(message.chat.id) + '/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            #os.chdir('/home/danila/video/video_maker_on_python/vid/user_' + str(message.chat.id) + '/') не убирать на случай если что-то в функции опять сломается
            print(os.getcwd())
            derect_function.rename_imgfile(message.chat.id, message.document.file_name, start_dir)


        bot.reply_to(message, "Фото сохранено")
    except Exception as e:
        bot.reply_to(message, e)

bot.polling(none_stop=True)