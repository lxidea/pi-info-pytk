#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys,time,json,threading
import datetime, Queue
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *
#import requests
import tkMessageBox

global exitflag
global win
global inf
exitflag = False

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
        self.timevar = StringVar()
        self.datevar = StringVar()
        self.width = self.tk.winfo_screenwidth()
        self.height = self.tk.winfo_screenheight() - 40
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
        self.timetext.grid(row=0,column=0)
        self.datetext.grid(row=1,column=0)
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
            return
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
        self.today = datetime.date.today()
        self.initThread()
    def initThread(self):
        global win
        self.thread = threading.Thread(target=self.wait2call,args=(win,))
        self.thread.setDaemon(True)
        self.thread.start()
    def destroy(self):
        self.thread.stop()
    def updateTime(self):
        self.today = datetime.date.today()
        self.year = self.today.strftime("%Y")
        self.month = self.today.strftime("%m")
        self.day = self.today.strftime("%d")
        self.week = self.today.strftime("%W")
        self.weekday = int(self.today.strftime("%w"))
        self.win.updateTime(self.composeTimeStr())
        self.win.updateDate(self.composeDateStr())
    def wait2call(self, FullW=None):
        #print FullW
        if FullW is not None:
            self.win = FullW
        elif self.win is None:
            raise Exception("None Fullscreen Window handle")
        if exitflag:
            self.thread.stop()
        while True:
            self.updateTime()
            time.sleep(1)
            if exitflag:
                break
        self.thread.stop()
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
