import telebot
from telebot import types

import random
from random import randint

bot = telebot.TeleBot('*********************************')
markdown = """
*bold text*
_italic text_
[text](URL)
"""


d = {}

word = ''
translate = ''
ask = ''
g_key = ''
g_val = ''

with open('dict.txt', encoding = 'utf-8') as indict:
    for i in indict.readlines():
        key,val = i.strip().split(':')
        d[key] = val

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    if call.data == "yes":

        bot.send_message(call.message.chat.id, 'Запомню : )');

        d[word] = translate
        #сохранить в файл
        f = open('dict.txt', 'a+', encoding = 'utf-8')
        f.write("\n" + word +":"+ translate)
        f.close()

    elif call.data == "no":

        bot.send_message(call.message.chat.id, 'Забыли : )');



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in d:
        bot.send_message(message.from_user.id,d[message.text])

    elif message.text == "/start":

        bot.send_message(message.from_user.id, "Я *бот помошник* для изучения английского языка. "
                                               "В моем лексиконе пока что " + str(len(d)) + " слов. "
                                               "Введи слово и посмотри знаю ли я его, или напиши /ask и я проверю твои знания. "
                                               "Для увеличения моего словарного запаса введи /mem. Мои возможности описаны в /help.", parse_mode = "Markdown")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/start - приветствие \n/help  - помощь\n/ask    - проверь себя\n/mem - запомнить слово")
    elif message.text == "/ask":
        global g_key
        global g_val
        data = list(d.items())
        key,val = data[randint(0, len(d)-1)]
        print(key)
        print(val)
        g_key = key
        g_val = val
        bot.send_message(message.from_user.id, '"' + key + '" что это?')
        bot.register_next_step_handler(message, get_ask);

    elif message.text == "/mem":
        bot.send_message(message.from_user.id, 'Напиши английское слово')
        bot.register_next_step_handler(message, get_word);

    else:
        bot.send_message(message.from_user.id, 'слово "' + message.text + '" я не знаю.', parse_mode = 'html')
        bot.send_message(message.from_user.id, 'хочешь я его запомню? набери /mem')

def get_ask(message):
    global ask
    ask = message.text
    if ask == g_val:
        bot.send_message(message.from_user.id, '*отлично*, вы знаете это _слово_', parse_mode = "Markdown")
    else:
        bot.send_message(message.from_user.id, '*плохо*, _ответ неверный_', parse_mode = "Markdown")
        bot.send_message(message.from_user.id, 'правильный ответ "' + g_val + '"')

def get_word(message):
    global word
    word = message.text
    bot.send_message(message.from_user.id, 'Какой перевод для этого слова?')
    bot.register_next_step_handler(message, get_translate)

def get_translate(message):
    global translate
    translate = message.text

    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    bot.send_message(message.from_user.id, word + ' это ' + translate + '?', reply_markup=keyboard)

bot.polling(none_stop=True, interval=0)