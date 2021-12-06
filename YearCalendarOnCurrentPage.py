#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
VERSION: 4.1 of 2021-11-06
AUTHOR: BASTIAN ILSØ HOUGAARD. 
LICENSE: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY.

Parts of this script are taken from the MonthlyCalendar script from Rafferty River.
"""
######################################################
# imports
from __future__ import division # overrules Python 2 integer division
import sys
import locale
import calendar
import datetime
from datetime import date, timedelta
import csv
import platform

try:
    from scribus import *
except ImportError:
    print("This Python script is written for the Scribus \
      scripting interface.")
    print("It can only be run from within Scribus.")
    sys.exit(1)

os = platform.system()
if os != "Windows" and os != "Linux":
    print("Your Operating System is not supported by this script.")
    messageBox("Script failed",
        "Your Operating System is not supported by this script.",
        ICON_CRITICAL)	
    sys.exit(1)

python_version = platform.python_version()
if python_version[0:1] != "3":
    print("This script runs only with Python 3.")
    messageBox("Script failed",
        "This script runs only with Python 3.",
        ICON_CRITICAL)	
    sys.exit(1)


######################################################

def isValidDate(year, month, day):
    isValidDate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False
    return isValidDate
    
def replaceText(text, item):
    txtwidth = getTextLength(item)
    insertText(text, txtwidth, item)
    selectText(0,txtwidth, item)
    deleteText(item)

######################################################
def main():
    """ Application/Dialog loop with Scribus sauce around """
    try:
        statusMessage('Running script...')
        progressReset()
        selCount = scribus.selectionCount()
        items = []
        for i in range(selCount):
            item = scribus.getSelectedObject(i)    
            type = scribus.getProperty(item,'itemType')
            if (type == 4):     
                items.append(item)
        
        firstDay = calendar.MONDAY
        month = valueDialog('Specify month', 'Specify which month to generate from 1 (January) to 12 (December).',str(datetime.datetime.now().month))
        month = int(month)
        year = valueDialog('Specify year', 'Specify which year to generate (4 digits: YYYY).', str(datetime.datetime.now().year))
        year = int(year)
        
        month_start = 1 
        month_end = calendar.monthrange(year, month)[1]
        
        d_start = datetime.datetime(year, month, month_start).weekday()
        d_end = datetime.datetime(year, month, month_end).weekday()
        
        cal = [
            ['','','','','',''],
            ['','','','','',''],
            ['','','','','',''],
            ['','','','','',''],
            ['','','','','',''],
            ['','','','','',''],
            ['','','','','',''],
            ]
        
        weekno = 0
        for i in range(month_start, month_end+1):
            if (isValidDate(year, month, i)):
             weekday = datetime.datetime(year, month, i).weekday()
             cal[weekday][weekno] = str(i)
             if (weekday == calendar.SUNDAY):
                 weekno += 1 
        
        
        for item in items:
            contents = scribus.getAllText(item)
            if (contents.startswith('$d')):
                 v = contents[2:]
                 id = v.split('-')
                 weekday = int(id[0])-1
                 weekno = int(id[1])-1
                 try:
                    replaceText(cal[weekday][weekno], item)
                 except IndexError:
                     messageBox("Error", "Expected 6 rows and 7 columns. Month is incorrectly formated.\n" 'weekday: ' + str(weekday) +
                                 ', weekno: ' + str(weekno), icon=ICON_ERROR)
                 
    finally:
        if haveDoc() > 0:
            redrawAll()
        statusMessage('Done.')
        progressReset()

if __name__ == '__main__':
    main()

