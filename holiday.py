from datetime import datetime
from selenium import webdriver
import json
import time

with open("settings.json","r") as fobj:
    content = json.load(fobj)
    fobj.close() 

ovrwrt = content["ovrwrt"]
PATH = content["path"]
waitPeriod = content["chromiumWait"]
holidayCheckY = content["holidayCheck"]

def checkWeekends() -> bool:
    weekDay = datetime.today().weekday()
    if weekDay == 5 or weekDay == 6:
        return False
    else:
        return True

def checkTimings() -> bool:
    # 0915 - 1530
    timeNow = datetime.today()
    timeNowHours = int(timeNow.strftime("%H"))
    timeNowMinutes = int(timeNow.strftime("%M"))
    morning = True
    afternoon = True

    if timeNowHours == 9:
        if timeNowMinutes <= 15:
            morning = False
    if timeNowHours == 15:
        if timeNowMinutes > 30:
            afternoon = False
    if timeNowHours < 9:
        morning = False
    if timeNowHours >= 16:
        afternoon = False
    
    if morning and afternoon:
        return True
    else:
        return False
    
def checkHolidays() -> bool:

    url = "https://www.nseindia.com/products-services/equity-market-timings-holidays"
    dateToday = datetime.today()
    dateTodayYear = int(dateToday.strftime("%Y"))
    if ovrwrt == True:
        dateTodayYear = holidayCheckY - 1
    if dateTodayYear != holidayCheckY:
        driver = webdriver.Chrome(PATH)
        driver.get(url)
        time.sleep(waitPeriod)
        search = driver.find_element_by_id("holidayTable")
        search = search.text
        holi = search.split(" ")
        fmt = {"holidays" : []}
        fmt["holidays"] = holi

        with open("holidays.json","w") as fobj:
            json.dump(fmt,fobj)
            fobj.close()

        with open("settings.json","r") as fobj:
            content = json.load(fobj)
            fobj.close()

        content["holidayCheck"] = dateTodayYear
        
        with open("settings.json","w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()

        checkDate = datetime.today()
        checkDate = checkDate.strftime("%d-%b-%Y")
        if checkDate in holi:
            return False
        else:
            return True

    else:
        with open("holidays.json","r") as fobj:
            content = json.load(fobj)
            fobj.close()
        holi = content["holidays"]

    checkDate = datetime.today()
    checkDate = checkDate.strftime("%d-%b-%Y")
    if checkDate in holi:
        return False
    else:
        return True

def mainCheck() -> bool:

    t = checkTimings()
    w = checkWeekends()
    h = checkHolidays()

    with open("settings.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    ovrwrt = content["ovrwrt"]
    
    if ovrwrt:
        return True
    elif t and w and h:
        return True
    else:
        return False

