import os
import errno
from datetime import datetime
import json
import telebot
from telebot import types
import sqlite3
import time
bot = telebot.TeleBot('5238517183:AAHkdru03SWwWiPpvzSNFGLXRyXhWKl2wnw')


@bot.message_handler(commands=['start'])
def start(message):
    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Регистрация")
    btn2 = types.KeyboardButton("Авторизация")
    markup_main.add(btn1, btn2)

    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text='👋Добрый день, пройдите авторизацию', reply_markup=markup_main)


def make_sure_path_exists(path):
    try: os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def convert_to_binary_data(filename):
    file = open(filename, 'rb')
    blob_data = file.read()
    return blob_data

def convert_to_not_binary_data(data, filename):
    file = open(filename, 'wb')
    photo_name = file.write(data)
    return blob_data


@bot.message_handler(content_types=['text'])
def func(message):
    message_arr = message.text.split()

    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📸 Отчет")
    btn2 = types.KeyboardButton("📜 Примеры работ")
    btn3 = types.KeyboardButton("🗣️ Финансовый отдел")
    btn4 = types.KeyboardButton("🧾 График работы")
    btn5 = types.KeyboardButton("📑 Правила работы")
    markup_main.add(btn1, btn2, btn3, btn4, btn5)

    markup_return = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Вернуться в главное меню")
    markup_return.add(button1)

    markup_reg = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_reg = types.KeyboardButton("Регистрация")
    markup_reg.add(button1)

    if message.text == "📸 Отчет":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Пришлите в чат описание по примеру и фотографию, а потом вернитесь в главное меню:\n\nОписание\n(ВМ)Балашиха новая Павлина ул.Троицкая д2 кв186 под3 эт13. Александр.Сантехник. Установить ванну. Си нужен сегодня', reply_markup=markup_return)
        make_sure_path_exists(str(message.chat.id))

    elif message.text == "📜 Примеры работ":  # Говно
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text=f"Есть несколько готовых актов:\n_ТУТ ДОЛЖнЫ БЫТЬ ФОТОГРАФИИ_", reply_markup=markup_return)

    elif message.text == "🧾 График работы":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Пришлите график своей работы. Сообщение по примеру:\n\nГрафик\nРаб\n*Дни месяца через пробелы*\nВых\n*Дни месяца через пробелы*", reply_markup=markup_return)

    elif message.text == "🗣️ Финансовый отдел":  # Говно
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Для связи с куратором обратитесь сюда: \n@finotdelSC",reply_markup=markup_return)

    elif message.text == "📑 Правила работы": # Говно
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        with open('Rules.txt', 'r',encoding='utf8') as new_file:
            rule = new_file.read()
        bot.send_message(message.chat.id, text=f"Перечень правил работы:\n{rule}",reply_markup=markup_return)

    elif message.text == "Вернуться в главное меню":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup_main)

    elif str(message_arr[0]) == "Описание":
        count = 1
        message_text = ''
        while count < len(message_arr):
            message_text += str(message_arr[count]) + ' '
            count += 1
        file = open('file.txt', 'w')
        file.write(message_text)
        file.close()

    elif message.text == "Регистрация":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text='Пришлите ваше полное ФИО по примеру:\n\nФИО\n*Фамилия Имя Отчечство*')

    elif message_arr[0] == 'ФИО':
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)

        id = str(message.chat.id)
        text = message_arr[1] + ' ' + message_arr[2] + ' ' +  message_arr[3]
        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS UserInfo(id, FIO)')
        base.commit()
        cur.execute('INSERT INTO UserInfo VALUES(?, ?)', (id, text))
        base.commit()
        bot.send_message(message.chat.id, text='Регистрация пройдена!', reply_markup=markup_return)

    elif message.text == "Авторизация":
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id)

        id = str(message.chat.id)
        base = sqlite3.connect('Registracia.db')
        cur = base.cursor()
        info_id_list = cur.execute('SELECT id FROM UserInfo').fetchall()

        count = 0
        while count < len(info_id_list):
            info_id = str(info_id_list[count][0])
            if id == info_id:
                true = 1
                break
            count += 1
        if true == 1:
            bot.send_message(message.chat.id, text='Узнаю вас', reply_markup=markup_return)
        else:
            bot.send_message(message.chat.id, text='Первый раз вас вижу. Пройдите регистрацию', reply_markup=markup_reg)

    elif message_arr[0] == "График":
        count = 2
        while count < len(message_arr):
            if message_arr[count] == 'Вых':
                break
            count += 1
        work_day = message_arr[2:count]
        rest_day = message_arr[count + 1:]
        # Это нужно в бд записать или куда-то отправить?



    else:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text="Я вас не понимаю. Попробуйте другую команду.", reply_markup=markup_return)


@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    markup_return = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Вернуться в главное меню")
    markup_return.add(button1)

    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(message.photo[2].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)

    id = str(message.chat.id)
    date_time = str(datetime.now())[:-7]
    photo = convert_to_binary_data(name)
    text = open('file.txt', 'r')
    text = text.read()


    base = sqlite3.connect('Registracia.db')
    cur = base.cursor()
    id_list = cur.execute('SELECT id FROM UserInfo').fetchall()
    name_list = cur.execute('SELECT FIO FROM UserInfo').fetchall()
    count = 0
    while count < len(id_list):
        info_id = str(id_list[count][0])
        if id == info_id:
            true = 1
            break
        count += 1
    table_name = str(name_list[count][0].replace(' ', ''))

    base = sqlite3.connect('test.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '(datetime TEXT, photo BLOB, text TEXT)')
    base.commit()
    cur.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?)', (date_time, photo, text))
    base.commit()
    os.remove(name)
    os.remove('file.txt')
    bot.delete_message(message.chat.id, message.message_id - 2)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, text="Отчет записан", reply_markup=markup_return)


bot.polling(none_stop=True)
