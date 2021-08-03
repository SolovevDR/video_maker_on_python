import telebot
from telebot import types
import os
import derect_function
import database
import command

bot = telebot.TeleBot('1555796929:AAHtJl5ELHE9jT6OUTXSUSEjRLKe1WIzmSk')

@bot.message_handler(commands=['start'])
def start(message):

    # keyboard
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Видео")
    item2 = types.KeyboardButton("Аудио")
    item3 = types.KeyboardButton("Завершить")
    item4 = types.KeyboardButton("/start")
    item5 = types.KeyboardButton("Добавить файлы")
    markup1.add(item1, item2).add(item3, item5).add(item4)

    start_dir = os.getcwd()

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
    derect_function.creat_com_dir(message.from_user.id)
    derect_function.creat_img_dir(message.from_user.id)
    derect_function.creat_res_dir(message.from_user.id)
    if database.select_status_of_usages(message.from_user.id) == 0:
        derect_function.delete_file_in_vid_dir(message.from_user.id)
        derect_function.delete_file_in_aud_dir(message.from_user.id)
        derect_function.delete_file_in_img_dir(message.from_user.id)
        derect_function.delete_file_in_res_dir(message.from_user.id)
        derect_function.creat_command_file(message.from_user.id)
    os.chdir(start_dir)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.chat.type == 'private':

        video_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Обрезать видео")
        item2 = types.KeyboardButton("Склеить видео")
        item3 = types.KeyboardButton("Добавить изображение")
        item4 = types.KeyboardButton("Конвертировать видео в чб")
        item5 = types.KeyboardButton("Извлечение аудио из видео")
        item6 = types.KeyboardButton("Отменить последнее действие")
        item7 = types.KeyboardButton("Назад")
        video_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6).add(item7)

        audio_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Наложение аудио поверх исходной дорожки")
        item2 = types.KeyboardButton("Наложение аудио убрав исходную дорожку")
        item3 = types.KeyboardButton("Редактирование громкости видео")
        item4 = types.KeyboardButton("Редактирование громкости аудио")
        item5 = types.KeyboardButton("Редактирование громкости видео на интервале")
        item6 = types.KeyboardButton("Обрезание аудио файла")
        item7 = types.KeyboardButton("Отменить последнее действие")
        item8 = types.KeyboardButton("Назад")
        audio_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6).add(item7).add(item8)

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Видео")
        item2 = types.KeyboardButton("Аудио")
        item3 = types.KeyboardButton("Завершить")
        item4 = types.KeyboardButton("/start")
        item5 = types.KeyboardButton("Добавить файлы")
        markup1.add(item1, item2).add(item3, item5).add(item4)

        if message.text == 'Видео': #and prov.back() == "0":
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами", reply_markup=video_keyboard)
            bot.register_next_step_handler(message, video_menu)
        elif message.text == 'Аудио':
            bot.send_message(message.chat.id, "тут инструкция по работе с данными инструментами", reply_markup=audio_keyboard)
            bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Добавить файлы':
            bot.send_message(message.chat.id, 'Можете добавить файлы')
        elif message.text == 'Завершить':
            bot.send_message(message.chat.id, "Ожидайте пока действия, которые вы указали на выполнения обрабатываются")
            bot.send_message(message.chat.id, "Это может занять некоторое время. Когда все обработается бот вам отправит результат")
            command.do_command_list(message.from_user.id)
            bot.send_message(message.chat.id, "Видео обработано, сейчас будут отправляться")
            start_dir = os.getcwd()
            dir_files = derect_function.checking_for_resalt(message.chat.id, start_dir)
            if len(dir_files) != 0:
                for i in range(len(dir_files)):
                    if '.mp4' in dir_files[i]:
                        os.chdir(os.getcwd() + '/res/user_' + str(message.chat.id) + '/')
                        video = open(dir_files[i], 'rb')
                        bot.send_video(message.chat.id, video)
                        video.close()
                        os.chdir(start_dir)
                    elif '.mp3' in dir_files[i]:
                        os.chdir(os.getcwd() + '/res/user_' + str(message.chat.id) + '/')
                        music = open(dir_files[i], 'rb')
                        bot.send_audio(message.chat.id, music)
                        music.close()
                        os.chdir(start_dir)
            else:
                os.chdir(os.getcwd() + '/vid/user_' + str(message.chat.id) + '/')
                dir_files = os.listdir()
                for i in range(len(dir_files)):
                    video = open(dir_files[i], 'rb')
                    bot.send_video(message.chat.id, video)
                    video.close()
                os.chdir(start_dir)
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                dir_files = os.listdir()
                for i in range(len(dir_files)):
                    audio = open(dir_files[i], 'rb')
                    bot.send_audio(message.chat.id, audio)
                    audio.close()
                os.chdir(start_dir)
            database.update_status_of_usages(message.chat.id, 0)
        elif message.text == '/start':
            item4 = types.KeyboardButton("/start")
            markup1.add(item4)
            bot.send_message(message.chat.id, 'Вы уверены, что хотите совершить данное действие? \n'
                             'Ваши файлы и выбранные команды в этом случае будут удалены')
        else:
            bot.send_message(message.chat.id, 'Ты ввел что-то не правильно',reply_markup=markup1)
            bot.register_next_step_handler(message, main_menu)


@bot.message_handler(content_types=['text'])
def video_menu(message):
    if message.chat.type == 'private':

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Видео")
        item2 = types.KeyboardButton("Аудио")
        item3 = types.KeyboardButton("Завершить")
        item4 = types.KeyboardButton("/start")
        item5 = types.KeyboardButton("Добавить файлы")
        markup1.add(item1, item2).add(item3, item5).add(item4)

        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item3 = types.KeyboardButton("Добавить еще")
        item4 = types.KeyboardButton("Закончить")
        markup2.add(item3, item4)

        if message.text == 'Обрезать видео': #and prov.back() == "0":
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '0', False)
            bot.send_message(message.chat.id, "Введите видео, которое вы хотите обрезать")
            bot.send_message(message.chat.id, "Если указанное окончание будет превышать длину ввидео, то видео "
                                              "будет обрезано только по вреени начала")
            bot.register_next_step_handler(message, number_cut_video)
        elif message.text == 'Склеить видео':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '1', False)
            bot.send_message(message.chat.id, "Введите порядок видео, в котором они будут добавлены", reply_markup=markup2)
            bot.register_next_step_handler(message, connect_video)
        elif message.text == 'Добавить изображение':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '2', False)
            bot.send_message(message.chat.id, "Введите номер изображения")
            bot.register_next_step_handler(message, number_image)
        elif message.text == 'Конвертировать видео в чб':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '3', False)
            bot.send_message(message.chat.id, "Введите номер видео")
            bot.register_next_step_handler(message, number_make_video_white_black)
        elif message.text == 'Извлечение аудио из видео':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '4', False)
            bot.send_message(message.chat.id, "Введите номер видео из которого нужно извлечь аудио")
            bot.register_next_step_handler(message, number_extract_audio_from_video)
        elif message.text == "Отменить последнее действие":
            database.update_last_use(message.chat.id)
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)
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
        item3 = types.KeyboardButton('Завершить')
        item4 = types.KeyboardButton("/start")
        item5 = types.KeyboardButton("Добавить файлы")
        markup1.add(item1, item2).add(item3, item5).add(item4)

        if message.text == 'Наложение аудио поверх исходной дорожки':  # and prov.back() == "0":
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '5', False)
            bot.send_message(message.chat.id, "выберете номер видео, на которое накладывается видео")
            bot.register_next_step_handler(message, number_video_for_audio_with_mute)
        elif message.text == 'Наложение аудио убрав исходную дорожку':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '6', False)
            bot.send_message(message.chat.id, "выберете номер видео, на которое накладывается видео")
            bot.register_next_step_handler(message, number_video_for_audio_without_mute)
        elif message.text == 'Редактирование громкости видео':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '7', False)
            bot.send_message(message.chat.id, "Выберете номер видео, громкость которого хотите изменить")
            bot.register_next_step_handler(message, number_editing_audio_in_video)
        elif message.text == 'Редактирование громкости аудио':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '8', False)
            bot.send_message(message.chat.id, "Выберете номер аудио, громкость которого хотите изменить")
            bot.register_next_step_handler(message, number_editing_audio_in_audio)
        elif message.text == 'Редактирование громкости видео на интервале':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '9', False)
            bot.send_message(message.chat.id, "Выберете номер видео, громкость на интервале которого хотите изменить")
            bot.register_next_step_handler(message, number_editing_audio_in_video_segment)
        elif message.text == 'Обрезание аудио файла':
            database.update_last_use(message.chat.id)
            derect_function.write_command_in_comad_file(message.chat.id, '10', False)
            bot.send_message(message.chat.id, "Выберете номер аудио, обрезать которое вы хотите")
            bot.register_next_step_handler(message, number_cut_audio)
        elif message.text == "Отменить последнее действие":
            database.update_last_use(message.chat.id)
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)
        elif message.text == 'Назад':
            bot.send_message(message.chat.id, "Назад", reply_markup=markup1)
            bot.register_next_step_handler(message, main_menu)
        else:
            bot.send_message(message.chat.id, 'Ты ввел что-то не правильно')
            bot.register_next_step_handler(message, audio_menu)


#функции для обрезания видео(вроде работает)
@bot.message_handler(content_types=['text'])
def number_cut_video(message):
    if message.chat.type == 'private':
        try:
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите время начала видео")
                bot.register_next_step_handler(message, start_video)
        except:
            bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
            bot.send_message(message.chat.id, "Начните данную операцию заново")
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)



@bot.message_handler(content_types=['text'])
def start_video(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время конца видео")
            bot.register_next_step_handler(message, end_video)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)


@bot.message_handler(content_types=['text'])
def end_video(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Время записано")
            bot.register_next_step_handler(message, video_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)


#функция для конвертирования видео в чб(вроде работает)
@bot.message_handler(content_types=['text'])
def number_make_video_white_black(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
                bot.send_message(message.chat.id, "Видео для конвертирования запомнено")
                bot.register_next_step_handler(message, video_menu)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)



#функции для добавления картинки к видео
@bot.message_handler(content_types=['text'])
def number_image(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_image_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Вы ввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите сколько по времени должно длиться изображение")
                bot.register_next_step_handler(message, len_image)
    except:
        bot.send_message(message.chat.id, "Вы ввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)

@bot.message_handler(content_types=['text'])
def len_image(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True

    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите номер видео до/после, которого будет добавлена картинка")
            bot.register_next_step_handler(message, number_video)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)

@bot.message_handler(content_types=['text'])
def number_video(message):
    try:

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("До")
        item2 = types.KeyboardButton("После")
        markup1.add(item1, item2)

        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Вы ввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите картинка должна быть добавлена до или"
                                                  " после видео", reply_markup=markup1)
                bot.register_next_step_handler(message, after_before_video)
    except:
        bot.send_message(message.chat.id, "Вы ввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)


@bot.message_handler(content_types=['text'])
def after_before_video(message):


        video_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Обрезать видео")
        item2 = types.KeyboardButton("Склеить видео")
        item3 = types.KeyboardButton("Добавить изображение")
        item4 = types.KeyboardButton("Конвертировать видео в чб")
        item5 = types.KeyboardButton("Извлечение аудио из видео")
        item6 = types.KeyboardButton("Отменить последнее действие")
        item7 = types.KeyboardButton("Назад")
        video_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6).add(item7)

        if message.chat.type == 'private':
            if message.text == 'До':
                derect_function.write_command_in_comad_file(message.chat.id, '0', True)
                bot.send_message(message.chat.id, "Действие записано", reply_markup=video_keyboard)
                bot.register_next_step_handler(message, video_menu)
            elif message.text == 'После':
                derect_function.write_command_in_comad_file(message.chat.id, '1', True)
                bot.send_message(message.chat.id, "Действие записано", reply_markup=video_keyboard)
                bot.register_next_step_handler(message, video_menu)
            else:
                bot.send_message(message.chat.id, "Вы ввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)



#функция для извлечения аудио из видео(вроде работает)(требует доработки)
@bot.message_handler(content_types=['text'])
def number_extract_audio_from_video(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
                bot.send_message(message.chat.id, "Видео для извлечения аудио запомнено")
                bot.register_next_step_handler(message, video_menu)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)



#функции для склейки видео
@bot.message_handler(content_types=['text'])
def connect_video(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, video_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Видео для склейки запомненно")
                bot.register_next_step_handler(message, connect_video_do)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)


@bot.message_handler(content_types=['text'])
def connect_video_do(message):

    video_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Обрезать видео")
    item2 = types.KeyboardButton("Склеить видео")
    item3 = types.KeyboardButton("Добавить изображение")
    item4 = types.KeyboardButton("Конвертировать видео в чб")
    item5 = types.KeyboardButton("Извлечение аудио из видео")
    item6 = types.KeyboardButton("Отменить последнее действие")
    item7 = types.KeyboardButton("Назад")
    video_keyboard.add(item1).add(item2).add(item3).add(item4).add(item5).add(item6).add(item7)

    if message.chat.type == 'private':
        if (message.text == 'Добавить еще'):
            bot.send_message(message.chat.id, "Введите следующее видео")
            bot.register_next_step_handler(message, connect_video)
        elif message.text == 'Закончить':
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', 'a')
            f.write('\n')
            f.close()
            bot.send_message(message.chat.id, "Порядок видео для склейки запомнено", reply_markup=video_keyboard)
            os.chdir(start_dir)
            bot.register_next_step_handler(message, video_menu)
        else:
            bot.send_message(message.chat.id, "Введите действие с клавиатуры")
            bot.register_next_step_handler(message, connect_video_do)


#функции для наложения музыкм без аудио(вроде работает)
@bot.message_handler(content_types=['text'])
def number_video_for_audio_with_mute(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите номер аудио, которое будет наложено")
                bot.register_next_step_handler(message, number_audio_with_mute)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def number_audio_with_mute(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_audio_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите время начала музыки")
                bot.register_next_step_handler(message, start_audio_with_mute)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def start_audio_with_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время конца музыки")
            bot.register_next_step_handler(message, end_audio_with_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def end_audio_with_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время начала фрагмента видео")
            bot.register_next_step_handler(message, start_video_with_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def start_video_with_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время конца фрагмента видео")
            bot.register_next_step_handler(message, end_video_with_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def end_video_with_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)



#функции для наложения аудио с музыкой(вроде работает)
@bot.message_handler(content_types=['text'])
def number_video_for_audio_without_mute(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите номер аудио, которое будет наложено")
                bot.register_next_step_handler(message, number_audio_without_mute)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def number_audio_without_mute(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_audio_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите время начала музыки")
                bot.register_next_step_handler(message, start_audio_without_mute)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def start_audio_without_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время конца музыки")
            bot.register_next_step_handler(message, end_audio_without_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def end_audio_without_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время начала фрагмента видео")
            bot.register_next_step_handler(message, start_video_without_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def start_video_without_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите время конца фрагмента видео")
            bot.register_next_step_handler(message, end_video_without_mute)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def end_video_without_mute(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)


#функции для редактирования громкости видео(вроде работает)
@bot.message_handler(content_types=['text'])
def number_editing_audio_in_video(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите коэфициент, на который хотите умножить гроскость видео")
                bot.send_message(message.chat.id, "Для уменьшенее громкости введите число от 0 до 1.\n"
                                                  "Для увелечения громкости введите число от 1 до 2")
                bot.register_next_step_handler(message, coefficient_to_change_video)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def coefficient_to_change_video(message):
    numbers = '0123456789.'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        counter = message.text.count('.')
        if counter >= 2:
            flag = False
        if message.text[0] == '.':
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)


#функция для редактирования громкости аудио(вроде работает)
@bot.message_handler(content_types=['text'])
def number_editing_audio_in_audio(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_audio_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите коэфициент, на который хотите умножить гроскость аудио")
                bot.send_message(message.chat.id, "Для уменьшенее громкости введите число от 0 до 1.\n"
                                                  "Для увелечения громкости введите число от 1 до 2")
                bot.register_next_step_handler(message, coefficient_to_change_audio)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def coefficient_to_change_audio(message):
    numbers = '0123456789.'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        counter = message.text.count('.')
        if counter >= 2:
            flag = False
        if message.text[0] == '.':
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)


#функции для редактирования громкости видео на заданном интервале(вроде работает)
@bot.message_handler(content_types=['text'])
def number_editing_audio_in_video_segment(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите коэфициент, на который хотите умножить гроскость аудио")
                bot.send_message(message.chat.id, "Для уменьшенее громкости введите число от 0 до 1.\n"
                                                  "Для увелечения громкости введите число от 1 до 2")
                bot.register_next_step_handler(message, coefficient_to_change_video_segment)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def coefficient_to_change_video_segment(message):
    numbers = '0123456789.'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        counter = message.text.count('.')
        if counter >= 2:
            flag = False
        if message.text[0] == '.':
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите начало фрагмента, на котором хотите уменьшить громкость")
            bot.register_next_step_handler(message, coefficient_to_change_start_video_segment)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def coefficient_to_change_start_video_segment(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите конец фрагмента, на котором хотите уменьшить громкость")
            bot.register_next_step_handler(message, coefficient_to_change_end_video_segment)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def coefficient_to_change_end_video_segment(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)


#функции для обрезания аудио(воде работает)
@bot.message_handler(content_types=['text'])
def number_cut_audio(message):
    try:
        if message.chat.type == 'private':
            if derect_function.checking_for_video_availability(message.chat.id, start_dir = os.getcwd()) < int(message.text):
                bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
                bot.send_message(message.chat.id, "Начните данную операцию заново")
                start_dir = os.getcwd()
                os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
                f = open('user_' + str(message.chat.id) + '.txt', "r")
                lines = f.readlines()
                f.close()
                f = open('user_' + str(message.chat.id) + '.txt', 'w')
                f.writelines([item for item in lines[:-1]])
                f.close()
                bot.send_message(message.chat.id, "Действие отменено")
                os.chdir(start_dir)
                bot.register_next_step_handler(message, audio_menu)
            else:
                derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
                bot.send_message(message.chat.id, "Введите начало аудио, с которого хотите начать")
                bot.register_next_step_handler(message, start_cut_audio)
    except:
        bot.send_message(message.chat.id, "Выввели данные, которых нет в системе")
        bot.send_message(message.chat.id, "Начните данную операцию заново")
        start_dir = os.getcwd()
        os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
        f = open('user_' + str(message.chat.id) + '.txt', "r")
        lines = f.readlines()
        f.close()
        f = open('user_' + str(message.chat.id) + '.txt', 'w')
        f.writelines([item for item in lines[:-1]])
        f.close()
        bot.send_message(message.chat.id, "Действие отменено")
        os.chdir(start_dir)
        bot.register_next_step_handler(message, video_menu)

@bot.message_handler(content_types=['text'])
def start_cut_audio(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, False)
            bot.send_message(message.chat.id, "Введите конец аудио, с которого хотите начать")
            bot.register_next_step_handler(message, end_cut_audio)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)

@bot.message_handler(content_types=['text'])
def end_cut_audio(message):
    numbers = '0123456789:,.'
    numberss = '0123456789'
    flag = True
    if message.chat.type == 'private':
        for i in range(len(message.text)):
            if (message.text[i] not in numbers):
                flag = False
        if message.text[0] not in numberss:
            flag = False
        if flag == True:
            derect_function.write_command_in_comad_file(message.chat.id, message.text, True)
            bot.send_message(message.chat.id, "Действие записано")
            bot.register_next_step_handler(message, audio_menu)
        else:
            bot.send_message(message.chat.id, "Вы ввели что то неправильно")
            bot.send_message(message.chat.id, 'Введите действие заново')
            start_dir = os.getcwd()
            os.chdir(os.getcwd() + '/aud/user_' + str(message.chat.id) + '/')
            f = open('user_' + str(message.chat.id) + '.txt', "r")
            lines = f.readlines()
            f.close()
            f = open('user_' + str(message.chat.id) + '.txt', 'w')
            f.writelines([item for item in lines[:-1]])
            f.close()
            bot.send_message(message.chat.id, "Действие отменено")
            os.chdir(start_dir)
            bot.register_next_step_handler(message, audio_menu)












#НЕ ТРОГАТЬ ЭТО ПОКА. ТУТ ВСЕ РАБОТАЕТ. НЕ ТРЕБУЕТ ИЗМЕНЕНИЙ!!!!!!!!!!!
#функция для скачивание документов для обработки
@bot.message_handler(content_types=['video'])
def handle_docs_video(message):
    #try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        start_dir = os.getcwd()
        print(start_dir)
        src = os.getcwd() + '/vid/user_'+ str(message.chat.id) + '/' + message.video.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            #os.chdir('/home/danila/video/video_maker_on_python/vid/user_' + str(message.chat.id) + '/') не убирать на случай если что-то в функции опять сломается
            print(os.getcwd())
        derect_function.rename_vidfile(message.chat.id, message.video.file_name, start_dir)


        bot.reply_to(message, "Видео сохранено")
    #except Exception as e:
       # bot.reply_to(message, e)

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