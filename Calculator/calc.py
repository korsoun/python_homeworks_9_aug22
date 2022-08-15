import telebot
from telebot import types
import datetime

def evaling(text):
    res = eval(text)
    return res

def logger(user_name, message, msg):
    with open('botlogs.txt', 'a', encoding = 'utf-8') as logs:
        logs.writelines(f'{datetime.datetime.now()} Пользователь {user_name} отправил сообщение "{message.text}". Ответил "{msg.text}"\n')
# def start_mes (message):
#     bot.send_message(message.chat.id, "Приветик!\nЯ простенький калькулятор.\nНа самом деле я мало что умею, но попробую тебе помочь.\nОтправь 'что делать', чтобы узнать, как давать команды.")

token = '5520746207:AAH0R6eCkf-GaM_7R2G5qSxcqqqNzYgjAgw'

bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Привет! Япростенький калькулятор. Я мало что умею, на самом деле, но постараюсь тебе помочь. Чтобы узнать, как со мной работать, отправь /help.')
    user_name = message.from_user.username
    logger(user_name, message, msg)

@bot.message_handler(commands=['help'])
def send_instr(message):
    msg = bot.send_message(message.chat.id, 'Напиши "решить <выражение>". Для ввода выражения используй знаки +-*/, для возведения в степень комбинацию **.\nМогу решить пример с комплексными числами. Для ввода мнимой части используй букву j.')
    user_name = message.from_user.username
    logger(user_name, message, msg)

@bot.message_handler(content_types=['text'])
def solving(message):
    user_name = message.from_user.username
    if 'решить' in message.text:
        if 'j' in message.text:
            msg = bot.send_message(message.chat.id, f'{complex(evaling(message.text[7:]))}')
        else:
            msg = bot.send_message(message.chat.id,f'{round(evaling(message.text[7:]), 3)}')
    else:
        msg = bot.send_message(message.chat.id, "Я не понимаю. Посмотри правила через команду /help")
    logger(user_name, message, msg)

print('Бот запущен.')
bot.infinity_polling()