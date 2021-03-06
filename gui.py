#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys,time,json,threading
import datetime, Queue
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *
import tkMessageBox
import PIL.Image
import PIL.ImageTk
from utils import *
import os.path

global exitflag
global win
global inf
exitflag = False

SPECIAL_COND = {"100","103","104","406","407"}
SCALE = 150

class varHome:
    def __init__(self):
        self.timevar = StringVar()
        self.datevar = StringVar()
    def setTimevar(string):
        self.timevar.set(string)
    def setDatevar(string):
        self.datevar.set(string)

class Fullscreen_Window:
    def __init__(self):
        self.tk = Tk()
        self.bgcolor = "#f0f0f0"
        self.timevar = StringVar()
        self.datevar = StringVar()
        self.cond_now_dcvar = StringVar()
        self.temp_now_var = StringVar()
        self.cond_tomo_dcvar = StringVar()
        self.temp_tomo_var = StringVar()
        self.tomo_descvar = StringVar()
        self.cond_now_dcvar.set(u'未知')
        self.temp_now_var.set(u'°C - °C')
        self.cond_tomo_dcvar.set(u'未知')
        self.temp_tomo_var.set(u'°C - °C')
        self.tomo_descvar.set(u'今天天气')
        self.width = self.tk.winfo_screenwidth()
        self.width = 800
        self.height = self.tk.winfo_screenheight() - 40
        self.height = 480 - 40
        timewidth = self.width
        timeheight = self.height *4/10
        fontsize = timeheight * 72 / 96
        #print timewidth, timeheight, fontsize
        #fontsize = 20
        #self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.tk.geometry("{0}x{1}+-6+0".format(self.width-6, self.height))
        self.frame = Frame(self.tk,width=timewidth,height=timeheight)
        #self.frame.geometry("{0}x{1}+-20+0".format(timewidth,timeheight))
        self.frame.pack()
        self.timetext = Label(self.frame,font=("Segoe UI",fontsize-2),#bg='red',#width=timewidth/2,
                              #height=timeheight/2,
                              textvariable=self.timevar,text='c')
        self.datetext = Label(self.frame,font=("华文楷体",fontsize*3/7-4),#bg='blue',#width=timewidth/2,
                              #height=timeheight/2,
                              textvariable=self.datevar,text='c')
        self.timetext.grid(row=0,column=0,columnspan=6)
        self.datetext.grid(row=1,column=0,columnspan=6)
        self.cond_icon_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/999.png"))
        self.cond_icon = Label(self.frame,image=self.cond_icon_img)
        self.cond_icon.image = self.cond_icon_img
        self.cond_icon.grid(row=2,column=0,sticky=E+N+S,rowspan=3,columnspan=1)
        self.nowtext = Label(self.frame,font=("华文楷体",25),text=u'实时')
        self.nowtext.grid(row=2,column=1,sticky=W)
        self.cond_now_dc = Label(self.frame,font=("华文楷体",25),textvariable=self.cond_now_dcvar,text=u'未知')
        self.cond_now_dc.grid(row=3,column=1,sticky=W)
        self.temp_now = Label(self.frame,font=("华文楷体",25),textvariable=self.temp_now_var,text=u'')
        self.temp_now.grid(row=4,column=1,sticky=W)
        self.forecast_icon1_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/999.png").resize((SCALE,SCALE),PIL.Image.ANTIALIAS))
        self.forecast_icon1 = Label(self.frame,image=self.forecast_icon1_img)
        self.forecast_icon1.image = self.forecast_icon1_img
        self.forecast_icon1.grid(row=2,column=2,sticky=E+N+S,rowspan=3,columnspan=1)
        self.forecast_icon2_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/999.png").resize((SCALE,SCALE),PIL.Image.ANTIALIAS))
        self.forecast_icon2 = Label(self.frame,image=self.forecast_icon2_img)
        self.forecast_icon2.image = self.forecast_icon2_img
        self.forecast_icon2.grid(row=2,column=3,sticky=W+N+S,rowspan=3,columnspan=1)
        self.tomotext = Label(self.frame,font=("华文楷体",25),text=u'今天天气',textvariable=self.tomo_descvar)
        self.tomotext.grid(row=2,column=4,sticky=W)
        self.cond_tomo_dc = Label(self.frame,font=("华文楷体",25),textvariable=self.cond_tomo_dcvar,text=u'未知')
        self.cond_tomo_dc.grid(row=3,column=4,sticky=W)
        self.temp_tomo = Label(self.frame,font=("华文楷体",25),textvariable=self.temp_tomo_var,text=u'')
        self.temp_tomo.grid(row=4,column=4,sticky=W)
        #self.timetext.pack()
        #self.datetext.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        #self.tk.bind("<KeyPress>", self.onKeyPress)
        #self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
    #def setVarBind(self,var):
        #self.var = var
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"
    def setbg(self, color):
        if self.bgcolor == color:
            return
        self.bgcolor = color
        self.tk.config(bg=self.bgcolor)
        self.frame.config(bg=self.bgcolor)
        self.timetext.config(bg=self.bgcolor)
        self.datetext.config(bg=self.bgcolor)
        self.cond_icon.config(bg=self.bgcolor)
        self.nowtext.config(bg=self.bgcolor)
        self.cond_now_dc.config(bg=self.bgcolor)
        self.temp_now.config(bg=self.bgcolor)
        self.forecast_icon1.config(bg=self.bgcolor)
        self.forecast_icon2.config(bg=self.bgcolor)
        self.tomotext.config(bg=self.bgcolor)
        self.cond_tomo_dc.config(bg=self.bgcolor)
        self.temp_tomo.config(bg=self.bgcolor)
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    def onKeyPress(self, event=None):
        self.timevar.set(event.char)
        self.datevar.set(event.char + "d")
        if event==None:
            return "break"
        #if event.char == 'c':
        #    self.setColor()
        if event.char == 'q':
            self.tk.quit
            return "break"
        if event.char == "e":
            #self.timevar.set(event.char)
            print self.timevar
            #self.timevar = "e"
            #self.timetext.config(text = "e")
            #self.timevar.set("timeeee")
            #self.timetext["text"] = "eeee"
            print self.timetext["text"]
            #self.timetext.update()
            #self.en["text"] = "eeee"
            return "break"
    def setColor(self, color=None):
        if color == None or color=="":
            color = "#FFFFFF"
        self.frame.config(bg = color)
        return "break"
    def updateTime(self, timestr):
        self.timevar.set(timestr)
        return "break"
    def updateDate(self, datestr):
        self.datevar.set(datestr)
        return "break"
    def on_closing(self):
        global exitflag
        exitflag = True
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.tk.destory()
        return "break"

class info:
    def __init__(self, FullW=None):
        global win
        self.win = win
        if FullW is not None:
            self.win = FullW
        else:
            raise Exception("None Fullscreen Window handle")
        self.sunset = None
        self.sunrise = None
        self.today = datetime.date.today()
        self.Hew = Heweather()
        self.initThread()
    def initThread(self):
        global win
        f=open("pi-info-pytk.pid","w")
        f.write(str(datetime.datetime.now()))
        f.close()
        self.timethread = threading.Thread(target=self.wait2call,args=(win,))
        self.timethread.setDaemon(True)
        self.timethread.start()
        self.weatherthread = threading.Thread(target=self.wait4weather,args=(win,))
        self.weatherthread.setDaemon(True)
        self.weatherthread.start()
    def destroy(self):
        if os.path.exists("pi-info-pytk.pid"):
            os.remove("pi-info-pytk.pid")
        #self.timethread.stop()
        #self.weatherthread.stop()
        #for mythread in threading.enumerate():
        #    mythread.stop()
    def updateTime(self):
        self.today = datetime.date.today()
        self.year = self.today.strftime("%Y")
        self.month = self.today.strftime("%m")
        self.day = self.today.strftime("%d")
        self.week = self.today.strftime("%W")
        self.weekday = int(self.today.strftime("%w"))
        self.win.updateTime(self.composeTimeStr())
        self.win.updateDate(self.composeDateStr())
    def updatebg(self):
        lower = 17
        upper = 238
        now = datetime.datetime.now()
        if self.sunset is None:
            return
        sunset = self.sunset
        sunrise = self.sunrise
        todayss = now.replace(hour=int(sunset[:2])+2,minute=int(sunset[-2:]))
        todaysr = now.replace(hour=int(sunrise[:2]),minute=int(sunrise[-2:]))
        manuss = now.replace(hour=int(sunset[:2])+3,minute=int(sunset[-2:]))
        manusr = now.replace(hour=int(sunrise[:2])-1,minute=int(sunrise[-2:]))
        color = ''
        if now>todaysr and now<todayss:
            self.win.setbg("#f0f0f0")
        elif now>=todayss and now<=manuss:
            cnum = int(lower + (lower - upper + 0.0)/(manuss - todayss).total_seconds()*(now - manuss).total_seconds())
            ccode = hex(cnum).replace('x','')[-2:]
            color = '#' + ccode + ccode + ccode
            self.win.setbg(color)
        elif now>=manusr and now<=todaysr:
            cnum = int(upper + (upper - lower + 0.0)/(todaysr - manusr).total_seconds()*(now - todaysr).total_seconds())
            ccode = hex(cnum).replace('x','')[-2:]
            color = '#' + ccode + ccode + ccode
            self.win.setbg(color)
        else:
            self.win.setbg("#111111")
            color = "#111111"
    def isDayTimeNow(self,sunset,sunrise):
        now = datetime.datetime.now()
        todayss = now.replace(hour=int(sunset[:2]),minute=int(sunset[-2:]))
        todaysr = now.replace(hour=int(sunrise[:2]),minute=int(sunrise[-2:]))
        if now<todaysr or now>todayss:
            return False
        return True
    def updateWeather(self):
        if not self.Hew.getinfo("weather"):
            return
        sunset = self.Hew.forecast.get("daily_forecast")[0].get('ss')
        sunrise = self.Hew.forecast.get("daily_forecast")[0].get('sr')
        Daytime = self.isDayTimeNow(sunset,sunrise)
        self.sunrise = sunrise
        self.sunset = sunset
        self.win.tomo_descvar.set(self.Hew.now.get("location"))
        self.win.cond_now_dcvar.set(self.Hew.now.get("cond_txt"))
        self.win.temp_now_var.set(self.Hew.now.get("temp")+u'°C')
        tmpstring = self.Hew.forecast.get("daily_forecast")[0].get('cond_txt_d') + u'转' + self.Hew.forecast.get("daily_forecast")[0].get('cond_txt_n')
        self.win.cond_tomo_dcvar.set(tmpstring)
        tmpstring = self.Hew.forecast.get("daily_forecast")[0].get('tmp_min') + u'°C-' + self.Hew.forecast.get("daily_forecast")[0].get('tmp_max') + u'°C'
        self.win.temp_tomo_var.set(tmpstring)
        tmpcode = self.Hew.now.get("cond_code")
        if tmpcode in SPECIAL_COND and Daytime is False:
            tmpcode = tmpcode + u'n'
        self.win.cond_icon_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/"+tmpcode+".png").resize((SCALE,SCALE),PIL.Image.ANTIALIAS))
        self.win.cond_icon.configure(image = self.win.cond_icon_img)
        self.win.cond_icon.image = self.win.cond_icon_img
        tmpcode = self.Hew.forecast.get("daily_forecast")[0].get("cond_code_d")
        if tmpcode in SPECIAL_COND and Daytime is False:
            tmpcode = tmpcode + u'n'
        self.win.forecast_icon1_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/"+tmpcode+".png").resize((SCALE,SCALE),PIL.Image.ANTIALIAS))
        self.win.forecast_icon1.configure(image = self.win.forecast_icon1_img)
        self.win.forecast_icon1_img = self.win.forecast_icon1_img
        tmpcode = self.Hew.forecast.get("daily_forecast")[0].get("cond_code_n")
        if tmpcode in SPECIAL_COND and Daytime is False:
            tmpcode = tmpcode + u'n'
        self.win.forecast_icon2_img = PIL.ImageTk.PhotoImage(PIL.Image.open("cond_icon_heweather/"+tmpcode+".png").resize((SCALE,SCALE),PIL.Image.ANTIALIAS))
        self.win.forecast_icon2.configure(image = self.win.forecast_icon2_img)
        self.win.forecast_icon2_img = self.win.forecast_icon2_img
    def wait2call(self, FullW=None):
        #print FullW
        if FullW is not None:
            self.win = FullW
        elif self.win is None:
            raise Exception("None Fullscreen Window handle")
        if not os.path.exists("pi-info-pytk.pid"):
            self.timethread.exit()
        bgsleeper = 0
        while True:
            if bgsleeper==10:
                self.updatebg()
            else:
                bgsleeper += 1
                if bgsleeper >= 11:
                    bgsleeper = 0
            self.updateTime()
            time.sleep(1)
            if exitflag:
                break
        self.timethread.stop()
    def wait4weather(self, FullW=None):
        #print FullW
        if FullW is not None:
            self.win = FullW
        elif self.win is None:
            raise Exception("None Fullscreen Window handle")
        if not os.path.exists("pi-info-pytk.pid"):
            self.weatherthread.exit()
        while True:
            self.updateWeather()
            time.sleep(3600)
            if exitflag:
                break
        self.weatherthread.stop()
    def composeTimeStr(self):
        timestr = datetime.datetime.now().strftime("%H:%M:%S")
        #print timestr
        return timestr
    def composeDateStr(self):
        weekstr = [u"日",u"一",u"二",u"三",u"四",u"五",u"六"]
        datestr = u"{0}年{1}月{2}日 星期{3}".format(self.year,self.month,self.day,weekstr[self.weekday])
        #print datestr
        return datestr

if __name__ == '__main__':
    global win,inf
    win = Fullscreen_Window()
    inf = info(win)
    #inf.updateTime(win)
    #v = varHome()
    #w.setVarBind(v)
    #w.setColor()
    #time.sleep(1)
    #w.setColor("#121212")
    win.tk.mainloop()
    inf.destroy()
