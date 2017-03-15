# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:10:46 2017

@author: guida
"""
from telebot import *
from sonarr import *
import time
import config
import logging

# Logging system Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('telegram-raspy.log', mode='w')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('---------------Telegram-Raspy------------')
logger.info('Adding personal info(Token,API and Chat_id)')
TOKEN = config.TOKEN
SONARR_API = config.SONARR_API
CHAT_ID = config.CHAT_ID

logger.info('Initializing telegram bot and sonarr parser')
telegram = bot(TOKEN)
sonarr = sonarr(SONARR_API)


def tel_sonarr_calendar():
    text = []
    calendar = sonarr.get_calendar()
    for series in calendar:
        text.append("--{} - {}  -{}".format(series['title']
                                            , series['episode'], series['date']))
    message = "\n".join(text)
    telegram.send_message(message, CHAT_ID)


def tel_sonarr_grabbed():
    grabbed = sonarr.get_history()
    text = []
    for episode in grabbed:
        text.append("--{} - {}".format(episode['title'], episode['episode']))
    message = "\n".join(text)
    telegram.send_message(message, CHAT_ID)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        logger.info('Message says: "%s"', text)
        if text == "/sonarr":
            keyboard = telegram.build_keyboard(['Sonarr grabbed', 'Sonarr calendar'])
            telegram.send_message("Select an option", CHAT_ID, keyboard)

        elif text == "/start":
            keyboard = telegram.build_keyboard(['/sonarr'])
            telegram.send_message("Server Manager", CHAT_ID, keyboard)
        elif text == "Sonarr calendar":
            logger.info('SCRIPT: Sending Sonarr calendar')
            tel_sonarr_calendar()
        elif text == "Sonarr grabbed":
            logger.info('SCRIPT: Sending Sonarr grabbed history')
            tel_sonarr_grabbed()
        else:
            logger.info('Message not understood')
            telegram.send_message("Sorry, I didn't understand you", CHAT_ID)


def main():
    logger.info('Initialized')
    last_update_id = None
    while True:
        updates = telegram.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            logger.info('Message received, Update_id: %s', str(last_update_id))
            last_update_id = telegram.get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
