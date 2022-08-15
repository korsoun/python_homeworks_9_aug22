import telebot
from telebot import types
import datetime
import re
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

token = '5118185695:AAGNpNLxeZGOjrLuZOWfUb4rKHRBVdPhfvg'
bot=telebot.TeleBot(token)

def get_pb_list():
    phonebook_list = []
    with open('phonebook.txt', 'r', encoding = 'utf-8') as pb:
        for line in pb:
            line = line[0:len(line)-1]
            line_lst = re.split(" - | ", line)
            phonebook_list.append(line_lst)
    return phonebook_list

def all_string_output ():
    whole_pb = get_pb_list()
    msg_text = ''
    for i in range(len(whole_pb)):
        for j in range(len(whole_pb[i])):
            msg_text += (f'{whole_pb[i][j]}\n')
        msg_text += f'\n'
    return msg_text

def person_output():
    whole_pb = get_pb_list()
    msg_text = ''
    for person in whole_pb:
        person_text = (' '.join(person))
        msg_text += f'{person_text}\n'
    return msg_text

def get_position (pos_to_find):
    request_lst = []
    with open('phonebook.txt', 'r', encoding = 'utf-8') as phonebook:
        for line in phonebook:
            if pos_to_find.upper() in line.upper():
                request_lst.append(line[:len(line)-1])
    return request_lst

def append_position (append_request):
    request_lst = append_request.split()
    with open('phonebook.txt', 'a', encoding = 'utf-8') as phonebook:
        phonebook.writelines(f'{request_lst[0]} {request_lst[1]} - {request_lst[2]} - {request_lst[3]}\n')

def rewrite_person (rewrite_req, rewrite_data, new_data):
    rewrite_list = re.split(" - | ", rewrite_req)
    if rewrite_data == 'и':
        req_position = 0
    elif rewrite_data == 'ф':
        req_position = 1
    elif rewrite_data == 'н':
        req_position = 2
    elif rewrite_data == 'к':
        req_position = 3
    pbread = open('phonebook.txt', 'r', encoding = 'utf-8')
    data = pbread.read()
    data = data.split('\n')
    for i in range(len(data)):
        if (rewrite_list[0] and rewrite_list[1] and rewrite_list[2] and rewrite_list[3]) in data[i]:
            data[i] = data[i].replace(rewrite_list[req_position], new_data)
    pbread.close()
    pbwrite = open('phonebook.txt', 'w', encoding = 'utf-8')
    for i in range(len(data)):
        pbwrite.write(str(f'{data[i]}\n'))
    pbwrite.close()
    
def delete_person (delete_req):
    pbread = open('phonebook.txt', 'r', encoding = 'utf-8')
    data = pbread.read()
    data = data.split('\n')
    for i in range(len(data)):
        if delete_req in data[i]:
            data[i] = ''
    pbread.close()
    pbwrite = open('phonebook.txt', 'w', encoding = 'utf-8')
    for i in range(len(data)):
        pbwrite.write(str(f'{data[i]}\n'))
    pbwrite.close()
    pbread = open('phonebook.txt', 'r', encoding = 'utf-8')
    data = pbread.read().split('\n')
    pbread.close()
    pbwrite = open('phonebook.txt', 'w', encoding = 'utf-8')
    for i in range(len(data)):
        if data[i] != "":
            pbwrite.write(str(f'{data[i]}\n'))
    
def logger(user_name, message, msg):
    with open('botlogs.txt', 'a', encoding = 'utf-8') as logs:
        logs.writelines(f'{datetime.datetime.now()} Пользователь {user_name} отправил сообщение "{message.text}". Ответил "{msg.text}"\n')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Показать справочник")
    btn2 = types.KeyboardButton("Найти контакт")
    btn3 = types.KeyboardButton("Добавить контакт")
    btn4 = types.KeyboardButton("Изменить контакт")
    btn5 = types.KeyboardButton("Удалить контакт")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    msg = bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я помогу тебе с телефонной книжкой.\nВернуться в начало всегда можно по команде '/start'.\nВыбери, что ты хочешь сделать.".format(message.from_user), reply_markup=markup)
    user_name = message.from_user.username
    logger(user_name, message, msg)

@bot.message_handler(content_types=['text'])
def disp(message):
    if(message.text == "Показать справочник"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Контакт в строке")
        btn2 = types.KeyboardButton("Элемент в строке")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, text="Чтобы просмотреть справочник, выбери тип отображения.')", reply_markup=markup)
    elif(message.text == "Элемент в строке"):
        if len(all_string_output()) != 0:
            msg = bot.send_message(message.chat.id, all_string_output())
        else:
            msg = bot.send_message(message.chat.id, "Сейчас справочник пуст. Но ты можешь его заполнить.")
    elif(message.text == "Контакт в строке"):
        if len(all_string_output()) != 0:
            msg = bot.send_message(message.chat.id, person_output())
        else:
            msg = bot.send_message(message.chat.id, "Сейчас справочник пуст. Но ты можешь его заполнить.")
    elif(message.text == "Найти контакт"):
        msg = bot.send_message(message.chat.id, text='Напиши "найди <и какую-либо информацию о контакте>"')
    elif('найди' in message.text):
        pos_to_find = message.text[6:]
        if len(get_position(pos_to_find)) == 1:
            msg = bot.send_message(message.chat.id, f'Вот что нашел:\n{get_position(pos_to_find)}')
        elif len(get_position(pos_to_find)) > 1:
            bot.send_message(message.chat.id, 'Вот что нашел:')
            for person in get_position(pos_to_find):
                msg = bot.send_message(message.chat.id, (' '.join(person)))
        else:
            msg = bot.send_message(message.chat.id, "Не получается ничего найти по такому запросу. Уточни запрос.")
    elif(message.text == "Добавить контакт"):
        msg = bot.send_message(message.chat.id, 'Напиши "добавь <Имя Фамилия Телефон Комментарий>. Сообщение должно состоять из четырех частей, разделенных пробелом.')
    elif('добавь' in message.text):
        append_request = message.text[7:]
        append_position(append_request)
        msg = bot.send_message(message.chat.id, "Контакт добавлен.")
    elif(message.text == "Изменить контакт"):
        bot.send_message(message.chat.id, 'Чтобы изменть контакт напиши "измени <код изменяемой позиции> <данные контакта> на <новые данные>"')
        bot.send_message(message.chat.id, "Коды изменяемой позиции:\nи - имя, ф - фамилия, н - номер, к - комментарий.\nВ качестве данных контакта подойдет имя, фамилия или номер.\nЯ могу изменить за один раз только одну позицию.")
    elif('измени' in message.text):
        rewrite_dtype = message.text[7:8]
        rewrite_req = message.text[9:]
        rewrite_req_list = rewrite_req.split(' на ')
        new_data = rewrite_req_list[1]
        if rewrite_dtype != 'и' and rewrite_dtype != 'ф' and rewrite_dtype != 'н' and rewrite_dtype != 'к':
            msg = bot.send_message(message.chat.id, "Кажется, ты ошибся в запросе. Проверь код изменяемых данных.")
        else:
            rewrite_req = rewrite_req_list[0]
            if len(get_position(rewrite_req)) > 1:
                msg = bot.send_message(message.chat.id, "Воу! По такому запросу я нашел несколько контактов.\nПожалуйста, выбери из них один и перепиши запрос, прописав в запросе этот контакт целиком. ")
                for person in get_position(rewrite_req):
                    bot.send_message(message.chat.id, (' '.join(person)))
            elif len(get_position(rewrite_req)) == 0:
                msg = bot.send_message(message.chat.id, "Упс! Я ничего не нашел по такому запросу. Ты уверен, что такой контакт есть в справочнике? Если да, уточни запрос.")
            else:
                rewrite_person (get_position(rewrite_req)[0], rewrite_dtype, new_data)
                msg = bot.send_message(message.chat.id, "Изменил!")
    elif(message.text == 'Удалить контакт'):
        msg = bot.send_message(message.chat.id, 'Для удаления контакта напиши "удали <данные контакта>". В качестве данных контакта подойдет имя, фамилия или номер.')
    elif('удали' in message.text):
        delete_req = message.text[6:]
        if len(get_position(delete_req)) > 1:
                msg = bot.send_message(message.chat.id, "Воу! По такому запросу я нашел несколько контактов.\nПожалуйста, выбери из них один и перепиши запрос, прописав в запросе этот контакт целиком. ")
                for person in get_position(delete_req):
                    bot.send_message(message.chat.id, (' '.join(person)))
        elif len(get_position(delete_req)) == 0:
            msg = bot.send_message(message.chat.id, "Упс! Я ничего не нашел по такому запросу. Ты уверен, что такой контакт есть в справочнике? Если да, уточни запрос.")
        else:
            delete_person (get_position(delete_req)[0])
            msg = bot.send_message(message.chat.id, "Удалил!")        
    else:
        msg = bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")
    user_name = message.from_user.username
    logger(user_name, message, msg)

print('Бот запущен.')
bot.infinity_polling()