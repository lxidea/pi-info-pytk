#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetcher import fetcher
from webparser import webparser
from user import user
import json,time
import sys,urllib,urllib2,hashlib,base64,time,binascii

class Heweather(object):
    """Heweather information wrapper"""
    URLS={"weather":"https://free-api.heweather.com/s6/weather",
    "sunrise_set":"https://free-api.heweather.com/s6/solar/sunrise-sunset",
    "air":"https://free-api.heweather.com/s6/air",
    "lifestyle":"https://free-api.heweather.com/s6/weather/lifestyle",
    "realtime":"https://free-api.heweather.com/s6/weather/now"}
    def __init__(self, _url=None):
        super(Heweather, self).__init__()
        #self.parser = parser(_url)
        if _url is not None:
            self._json = json.loads(webparser(_url).text())
        else:
            self._json = None
        self.user = user()
    def getinfo(self,keyword):
        if not self.user.ok or len(self.user.key)==0:
            print "Please fill info in the config file"
            exit(1)
        if URLS.get(keyword) is None:
            print "Heweather keyword wrong"
            exit(1)
        _url = URLS.get(keyword) + "?location=" + self.user.location + "&key=" + self.user.key
    @staticmethod
    def sign(self, params, secret):
        canstring = ''
        params = sorted(params.items(), key=lambda item:item[0])
        for k,v in params:
            if( k != 'sign' and k != 'key' and v != ''):
                canstring +=  k + '=' + v + '&'
        canstring = canstring[:-1]
        canstring += secret
        md5 = hashlib.md5(canstring).digest()
        return base64.b64encode(md5)
    @staticmethod
    def timestamp(self):
        return int(time.time())

if __name__ == '__main__':
    jnh = Heweather()#"https://free-api.heweather.com/s6/weather?location=%E6%AD%A6%E6%B1%89&key=7b000f53d48b4274a6ed074dae3b92d8")
    #myparser = parser(page)
