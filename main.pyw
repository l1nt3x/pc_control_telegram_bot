import os
from time import time
import ctypes
import telebot
from infi.systray import SysTrayIcon

try:
    from bot_config import ID, TOKEN, ICON_ICO, ICON_PNG
except Exception as e:
    print(e)
    bot_config_file = open('bot_config.py', 'w')
    bot_config_file.write("TOKEN = 'https://t.me/BotFather'\n")
    bot_config_file.write("ID = 'https://t.me/username_to_id_bot'\n")
    bot_config_file.write("ICON_ICO = 'iconname.ico'\n")
    bot_config_file.write("ICON_PNG = 'iconname.png'\n")
    ctypes.windll.user32.MessageBoxW(0, "NO CONFIG DEFINED! PLEASE EDIT bot_config.py", "WARNING!", 1)
    quit()

if ID == 'https://t.me/username_to_id_bot' or TOKEN == 'https://t.me/BotFather' or ICON_PNG == 'iconname.png' or ICON_ICO == 'iconname.ico':
    ctypes.windll.user32.MessageBoxW(0, "NO CONFIG DEFINED! PLEASE EDIT bot_config.py", "WARNING!", 1)
    quit()

bot = telebot.TeleBot(TOKEN)

TOKEN = TOKEN
ID = int(ID)

action = {
    'state': False,
    'time': 0.0
}

# keyboard
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = telebot.types.KeyboardButton("Завершение работы")
item2 = telebot.types.KeyboardButton("Перезагрузка")
item3 = telebot.types.KeyboardButton("Отмена")

markup.add(item1)
markup.add(item2)
markup.add(item3)


@bot.message_handler(commands=['start'])
def welcome(message):
    global ID
    global markup
    sti = open(ICON_PNG, 'rb')
    bot.send_sticker(message.chat.id, sti)
    user_id = message.from_user.id

    if user_id != ID:
        bot.send_message(message.chat.id, 'Вы не мой Хозяин :(')
        return 'Wrong ID'

    bot.send_message(ID,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для управления Вашим компьютером с помощью Telegram".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['code'])
def get_code(message):
    global markup
    global ID
    sti = open('github.png', 'rb')
    bot.send_sticker(message.chat.id, sti)
    if message.chat.id == ID:
        bot.send_message(message.chat.id,
                         '<a href="https://github.com/l1nt3x/pc_control_telegram_bot">l1nt3x/pc_control_telegram_bot</a>',
                         parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         '<a href="https://github.com/l1nt3x/pc_control_telegram_bot">l1nt3x/pc_control_telegram_bot</a>',
                         parse_mode='html')


@bot.message_handler(content_types=['text'])
def dialogue(message):
    global ID
    global markup
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
                    bot.send_message(ID, 'Завершение работы через 1 минуту. Чтобы отменить нажмите "Отмена"',
                                     reply_markup=markup)
                    os.system("shutdown -s -t 60")
                else:
                    bot.send_message(ID, 'Ещё выполняется предыдущая задача', reply_markup=markup)
            else:
                action['state'] = True
                action['time'] = time()
                bot.send_message(ID, 'Завершение работы через 1 минуту. Чтобы отменить нажмите "Отмена"',
                                 reply_markup=markup)
                os.system("shutdown -s -t 60")
        elif message.text == 'Перезагрузка':
            if action['state']:
                if abs(time() - action['time']) > 65:
                    action['state'] = True
                    action['time'] = time()
                    bot.send_message(ID, 'Перезагрузка через 1 минуту. Чтобы отменить нажмите "Отмена"',
                                     reply_markup=markup)
                    os.system("shutdown -r -t 60")
                else:
                    bot.send_message(ID, 'Ещё выполняется предыдущая задача', reply_markup=markup)
            else:
                action['state'] = True
                action['time'] = time()
                bot.send_message(ID, 'Перезагрузка через 1 минуту. Чтобы отменить нажмите "Отмена"',
                                 reply_markup=markup)
                os.system("shutdown -r -t 60")
        elif message.text == 'Отмена':
            if action['state']:
                action['state'] = False
                action['time'] = 0
                bot.send_message(ID, 'Отмена действия', reply_markup=markup)
                os.system("shutdown -a")
            else:
                bot.send_message(ID, 'Нет выполняемых задач', reply_markup=markup)
        else:
            bot.send_message(ID, 'Я не понимаю Вас', reply_markup=markup)


def on_quit_callback():
    bot.stop_polling()


systray = SysTrayIcon(ICON_ICO, "PC Control Telegram BOT", on_quit=on_quit_callback)

# RUN
if __name__ == '__main__':
    bot.send_message(ID, 'Ваш компьютер включен!', reply_markup=markup)
    systray.start()
    bot.infinity_polling()
