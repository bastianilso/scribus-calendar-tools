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
    
def GetWeekDayLetter(year, month, day):
    week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    d = datetime.datetime(int(year), int(month), int(day))
    weekday = d.weekday() 
    weekday_string = week_days[weekday]
    return(weekday_string[:1])

def GetWeekNumber(year,month,week):
    ending_day    = calendar.monthrange(year, month)[1]
    initial_week  = int(datetime.date(year, month, 1).strftime("%V"))
    ending_week   = int(datetime.date(year, month, ending_day).strftime("%V"))
    
    if (initial_week > ending_week):
        initial_week = 1

    weekrange = range(int(initial_week), int(ending_week)+1)
    weeknumber = ''
    try:
        weeknumber = weekrange[int(week)-1]
        weeknumber = "{:02d}".format(weeknumber)
    except IndexError:
        weeknumber = ''
    
    return(weeknumber)

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
        
        month = valueDialog('Specify month', 'Specify which month to generate from 1 (January) to 12 (December).',str(datetime.datetime.now().month))
        month = int(month)
        year = valueDialog('Specify year', 'Specify which year to generate (4 digits: YYYY).', str(datetime.datetime.now().year))
        year = int(year)         
        content = []       
        
        for item in items:
                contents = scribus.getAllText(item)
                # Insert Date Numbers
                if (contents.startswith('$n')):
                    day = contents[2:]
                    if (isValidDate(year,month,day)):
                        replaceText(day, item)
                    else:
                        setText('', item)
                # Insert Week Days
                if (contents.startswith('$d')):
                    day = contents[2:]
                    if (isValidDate(year,month,day)):
                        w = GetWeekDayLetter(year,month,day)
                        replaceText(w, item)
                    else:
                        setText('', item)
                # Insert Week Numbers
                if (contents.startswith('$w')):
                    week = contents[2:]
                    wn = GetWeekNumber(year,month,week)
                    props = getPropertyNames(item, includesuper=True)
                    replaceText(wn, item)
             
    finally:
        if haveDoc() > 0:
            redrawAll()
        statusMessage('Done.')
        progressReset()

if __name__ == '__main__':
    main()

