import os
from time import time

import telebot
from infi.systray import SysTrayIcon

from config import ID, TOKEN

bot = telebot.TeleBot(TOKEN)

TOKEN = TOKEN
ID = ID

action = {
    'state': False,
    'time': 0.0
}


@bot.message_handler(commands=['start'])
def welcome(message):
    global ID
    sti = open('seal.png', 'rb')
    bot.send_sticker(message.chat.id, sti)
    user_id = message.from_user.id

    if user_id != ID:
        bot.send_message(message.chat.id, 'Вы не мой Хозяин :(')
        return 'Wrong ID'

    # keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Завершение работы")
    item2 = telebot.types.KeyboardButton("Перезагрузка")
    item3 = telebot.types.KeyboardButton("Отмена")

    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(ID,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для управления Вашим компьютером с помощью Telegram".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['code'])
def get_code(message):
    sti = open('github.png', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     '[l1nt3x/pc_control_telegram_bot](https://github.com/l1nt3x/pc_control_telegram_bot)',
                     parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def dialogue(message):
    global ID
    user_id = message.from_user.id
    if user_id != ID:
        bot.send_message(message.chat.id, 'Вы не мой Хозяин :(')
        return 'Wrong ID'
    if message.chat.type == 'private':
        if message.text == 'Завершение работы':
            if action['state']:
                if abs(time() - action['time']) > 65:
                    action['state'] = True
                    action['time'] = time()
                    bot.send_message(ID, 'Завершение работы через 1 минуту. Чтобы отменить нажмите "Отмена"')
                    os.system("shutdown -s -t 60")
                else:
                    bot.send_message(ID, 'Ещё выполняется предыдущая задача')
            else:
                action['state'] = True
                action['time'] = time()
                bot.send_message(ID, 'Завершение работы через 1 минуту. Чтобы отменить нажмите "Отмена"')
                os.system("shutdown -s -t 60")
        elif message.text == 'Перезагрузка':
            if action['state']:
                if abs(time() - action['time']) > 65:
                    action['state'] = True
                    action['time'] = time()
                    bot.send_message(ID, 'Перезагрузка через 1 минуту. Чтобы отменить нажмите "Отмена"')
                    os.system("shutdown -r -t 60")
                else:
                    bot.send_message(ID, 'Ещё выполняется предыдущая задача')
            else:
                action['state'] = True
                action['time'] = time()
                bot.send_message(ID, 'Перезагрузка через 1 минуту. Чтобы отменить нажмите "Отмена"')
                os.system("shutdown -r -t 60")
        elif message.text == 'Отмена':
            if action['state']:
                action['state'] = False
                action['time'] = 0
                bot.send_message(ID, 'Отмена действия')
                os.system("shutdown -a")
            else:
                bot.send_message(ID, 'Нет выполняемых задач')
        else:
            bot.send_message(ID, 'Я не понимаю Вас')


def on_quit_callback(systray):
    bot.stop_polling()


systray = SysTrayIcon("seal.ico", "PC Control Telegram BOT", on_quit=on_quit_callback)

# RUN
if __name__ == '__main__':
    bot.send_message(ID, 'Ваш компьютер включен!')
    systray.start()
    bot.infinity_polling()
