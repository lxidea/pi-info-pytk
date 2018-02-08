#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetcher import fetcher
from webparser import webparser
import json

class Heweather(object):
    """Heweather information wrapper"""
    URLS={"weather":"https://free-api.heweather.com/s6/weather",
    "sunrise_set":"https://free-api.heweather.com/s6/solar/sunrise-sunset",
    "air":"https://free-api.heweather.com/s6/air",
    "lifestyle":"https://free-api.heweather.com/s6/weather/lifestyle",
    "realtime":"https://free-api.heweather.com/s6/weather/now"}
    def __init__(self, _url):
        super(Heweather, self).__init__()
        #self.parser = parser(_url)
        self._json = json.loads(webparser(_url).text())
        

if __name__ == '__main__':
    jnh = Heweather("https://free-api.heweather.com/s6/weather?location=%E6%AD%A6%E6%B1%89&key=7b000f53d48b4274a6ed074dae3b92d8")
    #myparser = parser(page)
