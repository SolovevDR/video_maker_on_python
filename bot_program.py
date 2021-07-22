import telebot
from telebot import types
import os
import derect_function

bot = telebot.TeleBot('1555796929:AAHtJl5ELHE9jT6OUTXSUSEjRLKe1WIzmSk')

@bot.message_handler(commands=['start'])
def start(message):

    # keyboard
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать")
    markup1.add(item1)

    bot.send_message(message.chat.id, "Это очередная хуйня, которая наверняка будет опять не закончена", reply_markup=markup1)


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
            derect_function.creat_dir(message.chat.id)

            #bot.register_next_step_handler(message, actiom_1)
        else:

            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("ты даже тут облажался")
            markup1.add(item1)

            bot.send_message(message.chat.id, 'Ты ввел какую то хуйню',reply_markup=markup1)


@bot.message_handler(content_types=['video'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(os.getcwd())

        start_dir = os.getcwd()
        src = os.getcwd() + '/vid/user_'+ str(message.chat.id) + '/' + message.video.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            #os.chdir('/home/danila/video/video_maker_on_python/vid/user_' + str(message.chat.id) + '/') не убирать на случай если что-то в функции опять сломается
            print(os.getcwd())
            derect_function.rename_file(message.chat.id, message.video.file_name, start_dir)


        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True)