#Sonarr API
from modules import *


class sonarr():
    URL = "http://localhost:8989/api"

    def __init__(self,API,URL=URL):
        self.api=API
        self.url=URL

    def get_history(self):
        url = self.url + "/history?apikey={}&sortKey(date)&sortDir(desc) \
        &pageSize=4&filterKey=eventType&filterValue=3".format(self.api)
        js = get_json_from_url(url)
        return self.parse_grabbed_history(js)
    
    def parse_grabbed_history(self,jsHist):
        grabbed = []
        for record in jsHist['records']:
            title = record['series']['title']
            episode = 'S'+str(record['episode']['seasonNumber']) + \
            'E'+str(record['episode']['episodeNumber'])
            grabbed.append({'title':title,'episode':episode})
        return grabbed

    def get_calendar(self):
        url = self.url + "/calendar?apikey={}".format(self.api)
        js = get_json_from_url(url)
        return self.parse_calendar(js)
        
    def parse_calendar(self,jsCalend):
        calend = []
        for record in jsCalend:
            title = record['series']['title']
            episode = 'S'+str(record['seasonNumber']) + \
            'E'+str(record['episodeNumber'])
            date = record['airDate']
            calend.append({'title':title,'episode':episode,'date':date})
        return calend
            
