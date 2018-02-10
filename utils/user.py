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

class user(object):
    """docstring for user"""
    def __init__(self):
        super(user, self).__init__()
        self.ok = True
        if not os.path.isfile("..\config.ini"):
            f = open("..\config.ini","w")
            f.writelines(INI_FILE)
            f.close()
            self.ok = False
            #raise Exception("config file not exists, automatically created. Please fill the proper values")
        with open("..\config.ini") as f:
            myconfig = f.read().decode(codetype).encode("utf-8")
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(myconfig))
        self.location = config.get('Heweather','location')
        self.key = config.get('Heweather','key')

if __name__ == '__main__':
    my = user()
    if my.ok:
        print "location:",my.location,"key:",my.key
    else:
        print "config file not exists, created automatically"
