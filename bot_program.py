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
    item1 = types.KeyboardButton("Видео")
    item2 = types.KeyboardButton("Аудио")
    markup1.add(item1, item2)

    bot.send_message(message.chat.id, "Привет. Это бот созданный для создания простых манипуляций с видео. \n"
                                      "Весь доступный функционал вы можете посмотреть на вкладках клавиатуры. \n"
                                      "Во избежание неполадок в результате взаимодействий с ботом, мы рекомендуем пользоваться только клавиатурой бота.")
    bot.send_message(message.chat.id, "Все ваши файлы будут удалены спустя 3 часа, отсчитывая с последнего вашего действия.\n"
                                      "Мы также рекомендуем удалить все файлы, с которыми вы работали после завершения вашего сеанся,"
                                      " для этого также будет кнопка на клавиатуре", reply_markup=markup1)
    bot.send_message(message.chat.id, "Можете загружать ваши файлы. Видео и другие файлы должны быть загружены "
                                      "в том порядке, в котором вы будете с ними работать", reply_markup=markup1)

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
def main_menu(message):
    if message.chat.type == 'private':

        video_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Обрезать видео")
        item2 = types.KeyboardButton("Склеить видео")
        item3 = types.KeyboardButton("Добавить изображение")
        item4 = types.KeyboardButton("Конвертировать видео в чб")
        item5 = types.KeyboardButton("Извлечение аудио из видео")
        item6 = types.KeyboardButton("Назад")
        video_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6)

        audio_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Наложение аудио поверх исходной дорожки")
        item2 = types.KeyboardButton("Наложение аудио убрав исходную дорожку")
        item3 = types.KeyboardButton("Редактирование громкости видео")
        item4 = types.KeyboardButton("Редактирование громкости аудио")
        item5 = types.KeyboardButton("Редактирование громкости видео на интервале")
        item6 = types.KeyboardButton("Обрезание аудио файла")
        item7 = types.KeyboardButton("Назад")
        audio_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6).add(item7)

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Видео")
        item2 = types.KeyboardButton("Аудио")
        markup1.add(item1, item2)

        if message.text == 'Видео': #and prov.back() == "0":
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами", reply_markup=video_keyboard)
            bot.register_next_step_handler(message, video_menu)
        elif message.text == 'Аудио':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами", reply_markup=audio_keyboard)
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, 'Ты ввел что-то не правильно',reply_markup=markup1)
            bot.register_next_step_handler(message, main_menu)


@bot.message_handler(content_types=['text'])
def video_menu(message):
    if message.chat.type == 'private':

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Видео")
        item2 = types.KeyboardButton("Аудио")
        markup1.add(item1, item2)

        if message.text == 'Обрезать видео': #and prov.back() == "0":
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            #bot.register_next_step_handler(message, video_menu)
        elif message.text == 'Склеить видео':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            #bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Добавить изображение':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            #bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Конвертировать видео в чб':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
        elif message.text == 'Назад':
            bot.send_message(message.chat.id, "Назад", reply_markup=markup1)
            bot.register_next_step_handler(message, main_menu)
        else:
            bot.send_message(message.chat.id, 'Ты ввел что-то не правильно')
            bot.register_next_step_handler(message, video_menu)


@bot.message_handler(content_types=['text'])
def audio_menu(message):
    if message.chat.type == 'private':

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Видео")
        item2 = types.KeyboardButton("Аудио")
        markup1.add(item1, item2)

        if message.text == 'Наложение аудио поверх исходной дорожки':  # and prov.back() == "0":
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            # bot.register_next_step_handler(message, video_menu)
        elif message.text == 'Наложение аудио убрав исходную дорожку':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            # bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Редактирование громкости видео':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
            # bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Редактирование громкости аудио':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
        elif message.text == 'Редактирование громкости видео на интервале':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
        elif message.text == 'Обрезание аудио файла':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами")
        elif message.text == 'Назад':
            bot.send_message(message.chat.id, "Назад", reply_markup=markup1)
            bot.register_next_step_handler(message, main_menu)
        else:
            bot.send_message(message.chat.id, 'Ты ввел что-то не правильно')
            bot.register_next_step_handler(message, audio_menu)


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