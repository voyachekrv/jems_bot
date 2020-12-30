import os
import time
import json
from datetime import datetime
from multiprocessing import *

import schedule
import telebot
from dotenv import load_dotenv

load_dotenv()

# API-токен бота (извлекается из файла переменных окружения)
API_TOKEN = os.getenv('API_TOKEN')

# Тексты сообщений
MESSAGES = {
    'morning': 'Пожалуйста, не забудьте написать о том, какие задачи вы планируете сделать сегодня.',
    'evening': 'Напишите, пожалуйста, кто какие задачи за сегодня сделал.'
}

bot = telebot.TeleBot(API_TOKEN)


def start_process(chat_id):
    """
    Запуск процесса обработки расписания отправки сообщения
    """

    Process(target=SendingHandler.schedule_handling, args=(chat_id,)).start()


def get_day_status():

    """
    Получение статуса текущего дня
    :return: Статус дня - выходной / рабочий / сокращённый
    """

    with open('./holidays.json') as json_file:
        data = json.load(json_file)

    current_date = str(datetime.date(datetime.now()))

    if current_date in data['holidays']:
        return 'holiday'
    elif current_date in data['preholidays']:
        return 'preholiday'
    else:
        return 'workday'


class SendingHandler:
    """
    Обработчик расписания отправки сообщения
    """

    @classmethod
    def schedule_handling(cls, chat_id):
        """
        Обработка расписания и вызов методов отправки сообщения по времени
        :param chat_id: ID чата, в который посылаются сообщения
        """

        schedule.every().day.at('10:00').do(lambda: SendingHandler.morning_message(chat_id, MESSAGES['morning']))

        schedule.every().day.at('17:00').do(
            lambda: SendingHandler.evening_message(chat_id, 'preholiday', MESSAGES['evening'])
        )

        schedule.every().day.at('18:00').do(
            lambda: SendingHandler.evening_message(chat_id, 'workday', MESSAGES['evening'])
        )

        while True:
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def morning_message(cls, chat_id, text):
        """
        Отправка сообщения в утренние часы
        :param chat_id: ID чата, в который посылается сообщение
        :param text: Текст сообщения
        """

        if get_day_status() != 'holiday':
            bot.send_message(chat_id, text)

    @classmethod
    def evening_message(cls, chat_id, day_status, text):
        """
        Отправка сообщения в вечерние часы
        :param chat_id: ID чата, в который посылается сообщение
        :param day_status: Статус дня - рабочий / нерабочий / сокращенный
        :param text: Текст сообщения
        """

        current_day_status = get_day_status()

        if (current_day_status != 'holiday') and (current_day_status == day_status):
            bot.send_message(chat_id, text)


# Обработка команды /start и запуск процесса отслеживания расписания
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот успешно запущен.')

    start_process(message.chat.id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
