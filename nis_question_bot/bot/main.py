# -*- coding: utf-8 -*-
"""
This is the main executable file of the Tolstoy Telegram bot
"""
import config
import telebot  # need to pip install pyTelegramBotAPI
import threading
import time

import pandas as pd
import re
import os
import logging  # todo: log with timestamps
import pickle
from pandas import ExcelWriter

STATIC_DIR = 'static'

#logging.basicConfig(level=logging.INFO, filename=config.LOG_FILENAME)

# todo: move all the meaningful work into functions


q_texts = {
    1: 'Опишите, пожалуйста, в одном коротком предложении ситуацию, которая происходит на картинке',
    2: '',
    3: '',
    4: '',
}

bot = telebot.TeleBot(config.TOKEN)
path = 'data.xlsx'

pictures=pd.read_excel(path, sheetname='pictures', index_col='pic_id')
queue=pd.read_excel(path, sheetname='queue', index_col='u_id')
log=pd.read_excel(path, sheetname='log', index_col='q_id')


def write_db():
    """ Save the whole database back to Excel """
    # todo: refactor to mySQL instead of Excel MASHA!
    writer = ExcelWriter(path)
    pictures.to_excel(writer,'pictures')
    queue.to_excel(writer,'queue')
    log.to_excel(writer,'log')
    writer.save()



#функции, которые отвечают за вопросы и ответ бота (везде, где есть @bot)
@bot.message_handler(commands=['start'])
def greeting1(message):
    """ Initiate a new dialogue for this particular user."""
    bot.send_message(message.chat.id, 'Здравствуйте. Этот бот задает вопросы' 
        + ', чтобы научиться понимать естественный язык и узнавать новое о мире. ' 
        + 'Его сделали Надя Катричева, Маша Шеянова и Альфия Бабий для семинара по НИС. ' 
        + 'Для того, чтобы ответить на вопрос, выберете команду /ask_me.')
    if message.chat.id not in queue.index:
        queue.loc[message.chat.id, 'q_type'] = 0
        write_db()

@bot.message_handler(commands=['ask_me'])
def asker(message):
    # todo: maybe choose question from types 2-4 if log is not empty
    q_type = 1
    q_row = pictures.sample(1).iloc[0]
    log_row = pd.Series({'q_type': 1, 'q_text': q_texts[1], 'pic_id': q_row.name, 
        'u_id': message.chat.id, 'time_ask': pd.to_datetime(time.time())})
    log.loc[len(log)] = log_row
    queue.loc[message.chat.id, 'q_type'] = 1
    write_db()
    task1 = q_texts[1] + ": " + q_row.pic_link
    bot.send_message(message.chat.id, task1)

# функция смотрит на две вещи: в каком состоянии находится пользователь, 
@bot.message_handler(content_types=["text"])
def thematic_response(message):
    """ This function gives user messages to dialogue manager
    and sends back to the user its response.
    """
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=False)


