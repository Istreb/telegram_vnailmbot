#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import telebot
import logging, sys
import logging.config
import sqlite3
import config

conn = sqlite3.connect(config.db)
logging.basicConfig(stream=sys.stderr)
logging.config.fileConfig(config.log_ini)
logger = logging.getLogger('wsgi')

bot = telebot.TeleBot(config.token,threaded=False)



def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size).decode("utf-8")
    update = telebot.types.Update.de_json(request_body)
    chek_user_settings(update.message.from_user.id)#добавить пользователя если нет
    bot.process_new_messages([update.message]) #обработчик запросов
    start_response('200 OK', [('Content-Type', 'text/html')]) #всегда нужно возвращать 200, иначе сервер будет считать, что сообщение не доставлено
    return ''


#добавить пользователя если нет
def chek_user_settings(user_id):
    c = conn.cursor()
    c.execute ("""select id from users where id='%s'""" % user_id)
    reply = c.fetchone()
    if not reply:
        c.execute ("""INSERT INTO users VALUES(%s) """ % user_id)
        conn.commit()

#показать описание бота
@bot.message_handler(commands=['help', 'start'])
def echo_message(message):
    bot.send_message(message.chat.id, 'Персональный бот Виктории Каличава. Если вы не Виктория, пожалуйста, выйдите из чата.')

#---    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
	bot.send_message(message.chat.id, 'приветики конфетики')
