#!/usr/bin/python

# Quick script to compare current working dir JPG files to specified directory (fileskeepdir).  If the filename doesn't exist in fileskeepdir, the script deletes the JPG file from the current dir
# Depends on copypics.py

import os
from datetime import date

from copypics import Picture

fileskeepdir = '../Pictures_Avi_6mo/NewPics/'

for file in os.listdir('.'):
    if file.find('JPG') > -1:
        pic = Picture(filename = file)
        if pic.findcreatedate() > date(2016, 07, 15):
            filekeep = fileskeepdir + pic.filename
            if os.path.exists(filekeep):
                pass
            else:
                os.remove(pic.filename)
                print pic.filename, " removed"
