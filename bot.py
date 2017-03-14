import time
import json
import modules as mod
import urllib
import sonarr

#We add our bot's TOKEN (its ID)
class bot:
    
    def __init(self,TOKEN):
        self.TOKEN = TOKEN
        self.URL = "https://api.telegram.org/bot{}/".format(TOKEN)

    def get_updates(self,offset=None):
        url = self.URL + "getUpdates" #getUpdates corresponds to the telegram API.
        if offset:
            url+= "?offset={}".format(offset)
        js= mod.get_json_from_url(url)
        return js
    
    def get_last_update_id(self,updates):
        updates_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)
    
    
    def get_last_chat_id_and_text(self,updates):
        num_updates = len(updates["result"]) #Telegram's Json gives a "result" for each update
        last_update = num_updates -1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    
    
    def send_message(self,text, chat_id,reply_markup=None):
        text = urllib.parse.quote_plus(text) #Translate text to an url compatible one.
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup()".format(reply_markup)
        mod.get_url(url)
    
    
    def build_keyboard(self,items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard":True}
        return json.dumps(reply_markup)