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

def GetWeekDayLetter(weekday):
    week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    weekday_string = week_days[weekday]
    return(weekday_string[:1])
    
def GetDayFromWeek(year, week, weekday):
    # Fx. 2023, 1, 1
    
    d =  year + "-" + week + "-" + weekday
    d = '2013'
    r = date.fromisocalendar(int(year), int(week), int(weekday))
    #d = datetime.datetime.strptime(d, '%Y')
    date_string = str(r.day) + "/" + str(r.month)
        
    return(date_string)    
    

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
        
        week = valueDialog('Specify week', 'Specify which week to generate from 1 to 52.',str(datetime.datetime.now().strftime("%V")))
        #week = int(week)
        year = valueDialog('Specify year', 'Specify which year to generate (4 digits: YYYY).', str(datetime.datetime.now().year))
        #year = int(year)         
        content = []       
        
        for item in items:
                contents = scribus.getAllText(item)
                # Insert Date Numbers
                if (contents.startswith('$n')):
                    weekday = contents[2:]
                    day = GetDayFromWeek(year, week, weekday)
                    replaceText(day, item)
                # Insert Week Days
                if (contents.startswith('$d')):
                    weekday = contents[2:]
                    w = GetWeekDayLetter(weekday)
                    replaceText(w, item)
                # Insert Week Numbers
                if (contents.startswith('$weekno')):
                    wn = week
                    replaceText(wn, item)
             
    finally:
        if haveDoc() > 0:
            redrawAll()
        statusMessage('Done.')
        progressReset()

if __name__ == '__main__':
    main()

