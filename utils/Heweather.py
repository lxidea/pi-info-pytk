#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetcher import fetcher
from webparser import webparser
from myuser import myuser
import json,time
import sys,urllib,urllib2,hashlib,base64,time,binascii

URLS={"weather":"https://free-api.heweather.com/s6/weather",
    "sunrise_set":"https://free-api.heweather.com/s6/solar/sunrise-sunset",
    "air":"https://free-api.heweather.com/s6/air",
    "lifestyle":"https://free-api.heweather.com/s6/weather/lifestyle",
    "realtime":"https://free-api.heweather.com/s6/weather/now",
    "forecast":"https://free-api.heweather.com/s6/weather/forecast"}

class Heweather(object):
    """Heweather information wrapper"""
    def __init__(self, _url=None):
        super(Heweather, self).__init__()
        #self.parser = parser(_url)
        if _url is not None:
            self._json = json.loads(webparser(_url).text())
        else:
            self._json = None
        self.user = myuser()
        self.forecast = dict()
        self.now = dict()
        self.airnow = dict()
        self.sun = dict()
        self.lifestyle = dict()
        self.weather = dict()
    def getinfo(self,keyword,depth=0,**kwargs):
        if not self.user.ok or len(self.user.key)==0:
            print "Please fill info in the config file"
            exit(1)
        if URLS.get(keyword) is None:
            print "Heweather keyword wrong"
            exit(1)
        _url = URLS.get(keyword) + "?location=" + self.user.location + "&key=" + self.user.key + "&lang=zh"
        self.infojson = json.loads(webparser(_url).text())
        return self.infoparser(keyword)
    def infoparser(self,keyword):
        if keyword == "weather":
            return self.weatherparser()
        elif keyword == "sunrise_set":
            return self.sunrisesetparser()
        elif keyword == "air":
            return self.airnowparser()
        elif keyword == "lifestyle":
            return self.lifestyleparser()
        elif keyword == "realtime":
            return self.weathernowparser()
        elif keyword == "forecast":
            return self.forecastparser()
        else:
            raise Exception("unknow keyword for info parser")
        return False

    def weatherparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.now.clear()
        self.now["location"] = self.infojson.get("HeWeather6")[0].get("basic").get("location")
        #get the location
        self.now["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.now["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.now["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.now["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.now["cloud"] = self.infojson.get("HeWeather6")[0].get("now").get("cloud")
        #how many amount of cloud now
        self.now["cond_code"] = self.infojson.get("HeWeather6")[0].get("now").get("cond_code")
        #code for the weather condition
        self.now["cond_txt"] = self.infojson.get("HeWeather6")[0].get("now").get("cond_txt")
        #description on the current weather condition
        self.now["feel"] = self.infojson.get("HeWeather6")[0].get("now").get("fl")
        #temperature feels like
        self.now["pcpn"] = self.infojson.get("HeWeather6")[0].get("now").get("pcpn")
        #amount of precipitation
        self.now["pressure"] = self.infojson.get("HeWeather6")[0].get("now").get("pres")
        #barometric pressure
        self.now["temp"] = self.infojson.get("HeWeather6")[0].get("now").get("tmp")
        #temperature reading in default unit (degree centigrade)
        self.now["visual"] = self.infojson.get("HeWeather6")[0].get("now").get("vis")
        #visibility(measured in kilometer)
        self.now["wind_deg"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_deg")
        #direction of the wind orientation(measured in degree)
        self.now["wind_dir"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_dir")
        #description of the wind direction
        self.now["wind_sc"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_sc")
        #wind strength
        self.now["wind_speed"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_spd")
        #the speed of the wind, measured in unit of kilometer per hour

        self.forecast.clear()
        self.forecast["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.forecast["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.forecast["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.forecast["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.forecast["daily_forecast"] = self.infojson.get("HeWeather6")[0].get("daily_forecast")
        #in default it will store a lists, in which three days of forecast will be stored as invidual dict, the keys are
        #cond_code_d,cond_code_n,cond_txt_d,cond_txt_n,date,hum,mr,ms,pcpn,pop,pres,sr,ss,tmp_max,tmp_min,uv_index,vis,wind_deg,wind_dir,wind_sc,wind_spd
        #and corresponding meanings as
        #condition code daytime,condition code night,condition description daytime,condition description night,date,humidity,moon rise,moon set,precipitation,
        #possibility of precipitation,barometric pressure,sunrise,sunset,max temperature,min temperature,UV index,visibility,wind orientation in degree,
        #wind direction description,wind strength,wind speed

        self.lifestyle.clear()
        self.lifestyle["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.lifestyle["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.lifestyle["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.lifestyle["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        for key, value in {"comfort":"comf","dress":"drsg","flu":"flu","sport":"sport","traval":"trav","uv":"uv","carwashing":"cw","air":"air"}.iteritems():
            if None is not self.infojson.get("HeWeather6")[0].get("lifestyle"):
                for item in self.infojson.get("HeWeather6")[0].get("lifestyle"):
                    if item.get("type") == value:
                        self.lifestyle[key] = (item.get("brf"),item.get("txt"))
                        break
                    else:
                        continue
                break

        self.sun.clear()
        self.sun["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.sun["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.sun["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.sun["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        sunlist = []
        for item in self.forecast["daily_forecast"]:
            sunriseset = dict()
            sunriseset["date"] = item.get("date")
            sunriseset["sr"] = item.get("sr")
            sunriseset["ss"] = item.get("ss")
            sunlist.append(sunriseset)
        self.sun["sunriseset"] = sunlist
        #store a lists, contains three days sunrise and sunset information, each day is one dict
        #which have the keys of "date", "sr", "ss"

        return True
    def sunrisesetparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.sun.clear()
        self.sun["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.sun["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.sun["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.sun["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.sun["sunriseset"] = self.infojson.get("HeWeather6")[0].get("sunrise_sunset")
        #store a lists, contains three days sunrise and sunset information, each day is one dict
        #which have the keys of "date", "sr", "ss"
        return True

    def weathernowparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.now.clear()
        self.now["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.now["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.now["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.now["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.now["cloud"] = self.infojson.get("HeWeather6")[0].get("now").get("cloud")
        #how many amount of cloud now
        self.now["cond_code"] = self.infojson.get("HeWeather6")[0].get("now").get("cond_code")
        #code for the weather condition
        self.now["cond_txt"] = self.infojson.get("HeWeather6")[0].get("now").get("cond_txt")
        #description on the current weather condition
        self.now["feel"] = self.infojson.get("HeWeather6")[0].get("now").get("fl")
        #temperature feels like
        self.now["pcpn"] = self.infojson.get("HeWeather6")[0].get("now").get("pcpn")
        #amount of precipitation
        self.now["pressure"] = self.infojson.get("HeWeather6")[0].get("now").get("pres")
        #barometric pressure
        self.now["temp"] = self.infojson.get("HeWeather6")[0].get("now").get("tmp")
        #temperature reading in default unit (degree centigrade)
        self.now["visual"] = self.infojson.get("HeWeather6")[0].get("now").get("vis")
        #visibility(measured in kilometer)
        self.now["wind_deg"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_deg")
        #direction of the wind orientation(measured in degree)
        self.now["wind_dir"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_dir")
        #description of the wind direction
        self.now["wind_sc"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_sc")
        #wind strength
        self.now["wind_speed"] = self.infojson.get("HeWeather6")[0].get("now").get("wind_spd")
        #the speed of the wind, measured in unit of kilometer per hour
        return True

    def lifestyleparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.lifestyle.clear()
        self.lifestyle["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.lifestyle["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.lifestyle["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.lifestyle["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        for key, value in {"comfort":"comf","dress":"drsg","flu":"flu","sport":"sport","traval":"trav","uv":"uv","carwashing":"cw","air":"air"}.iteritems():
            for item in self.infojson.get("HeWeather6")[0].get("lifestyle"):
                if item.get("type") == value:
                    self.lifestyle[key] = (item.get("brf"),item.get("txt"))
                    break
                else:
                    continue
            break
        return True

    def forecastparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.forecast.clear()
        self.forecast["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.forecast["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.forecast["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.forecast["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.forecast["daily_forecast"] = self.infojson.get("HeWeather6")[0].get("daily_forecast")
        #in default it will store a lists, in which three days of forecast will be stored as invidual dict, the keys are
        #cond_code_d,cond_code_n,cond_txt_d,cond_txt_n,date,hum,mr,ms,pcpn,pop,pres,sr,ss,tmp_max,tmp_min,uv_index,vis,wind_deg,wind_dir,wind_sc,wind_spd
        #and corresponding meanings as
        #condition code daytime,condition code night,condition description daytime,condition description night,date,humidity,moon rise,moon set,precipitation,
        #possibility of precipitation,barometric pressure,sunrise,sunset,max temperature,min temperature,UV index,visibility,wind orientation in degree,
        #wind direction description,wind strength,wind speed
        return True

    def airnowparser(self):
        if len(self.infojson.keys()) == 0:
            return False
        self.airnow.clear()
        self.airnow["update"] = self.infojson.get("HeWeather6")[0].get("update").get("loc")
        #update time
        self.airnow["parent_city"] = self.infojson.get("HeWeather6")[0].get("basic").get("parent_city")
        #the superior city
        self.airnow["admin_area"] = self.infojson.get("HeWeather6")[0].get("basic").get("admin_area")
        #the area to whom the location belongs
        self.airnow["status"] = self.infojson.get("HeWeather6")[0].get("status")
        #the status of the json file get from server, default is ok if nothing wrong happens
        self.airnow["air_now_city"] = self.infojson.get("HeWeather6")[0].get("air_now_city")
        #a dict store various overall properties of current city, the keyword are
        #aqi, qlty, main, pm25, pm10, no2, so2, co, o3, pub_time (with their meaning as)
        #aqi value, quality description, main polution, pm25 value, pm10 value, no2, so2, co ,o3, pub_time
        self.airnow["air_now_station"] = self.infojson.get("HeWeather6")[0].get("air_now_station")
        #in default it will store a lists, in which variable number of air station readings will be stored as invidual dict
        #with each dict, it will have the keys as follows:
        #air_sta, aqi, asid, co, lat, lon, main, no2, o3, pm10, pm25, pub_time, qlty, so2
        #and their physical meaning
        #air station name, aqi, air station id, co value, lattitude, longitude, main polution, no2, o3, pm10, pm25, pub_time, quality description, so2
        return True

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
