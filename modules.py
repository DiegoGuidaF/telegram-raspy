# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:17:11 2017

@author: guida
"""
import json
import requests

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#Json parser
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js