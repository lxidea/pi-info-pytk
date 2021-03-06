#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,io
import os.path
import sys

codetype = sys.getfilesystemencoding()
INI_FILE = """[Heweather]
location = 
key = 
"""

class myuser(object):
    """docstring for user"""
    def __init__(self):
        super(myuser, self).__init__()
        self.ok = True
        fname = ''
        if os.path.exists("utils"):
            fname = "config.ini"
        else:
            fname = "..\config.ini"
        if not os.path.isfile(fname):
            f = open(fname,"w")
            f.writelines(INI_FILE)
            f.close()
            self.ok = False
            #raise Exception("config file not exists, automatically created. Please fill the proper values")
        with open(fname) as f:
            myconfig = f.read().decode(codetype).encode("utf-8")
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(myconfig))
        self.location = config.get('Heweather','location')
        self.key = config.get('Heweather','key')

if __name__ == '__main__':
    my = myuser()
    if my.ok:
        print "location:",my.location,"key:",my.key
    else:
        print "config file not exists, created automatically"
