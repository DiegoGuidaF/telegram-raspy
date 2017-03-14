# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:10:46 2017

@author: guida
"""
from telebot import *
from sonarr import *
import time
import config

TOKEN = config.TOKEN
SONARR_API = config.SONARR_API
CHAT_ID = config.CHAT_ID

telegram = bot(TOKEN)
sonarr = sonarr(SONARR_API)

def tel_sonarr_calendar():
    text = []
    calendar = sonarr.get_calendar()
    for series in calendar:
        text.append("--{} - {}  -{}".format(series['title'] \
        ,series['episode'],series['date']))
    message = "\n".join(text)
    telegram.send_message(message,CHAT_ID)
    
def tel_sonarr_grabbed():
    grabbed = sonarr.get_history()
    text = []
    for episode in grabbed:
        text.append("--{} - {}".format(episode['title'],episode['episode']))
    message = "\n".join(text)
    telegram.send_message(message,CHAT_ID)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        if text == "/sonarr":
            keyboard = telegram.build_keyboard(['Sonarr grabbed','Sonarr calendar'])
            telegram.send_message("Select an option", CHAT_ID, keyboard)
            
        elif text == "/start":
            keyboard = telegram.build_keyboard(['/sonarr'])
            telegram.send_message("Server Manager", CHAT_ID, keyboard)
        elif text == "Sonarr calendar":
            tel_sonarr_calendar()
        elif text == "Sonarr grabbed":
            tel_sonarr_grabbed()
        else:
            telegram.send_message("Sorry, I didn't understand you",CHAT_ID)



def main():
    last_update_id = None
    while True:
        updates = telegram.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = telegram.get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
  main()