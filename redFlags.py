from selenium import webdriver
import json
import time

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

asmShort = []
asmLong = []
gsm = []

with open("settings.json","r") as fobj:
    content = json.load(fobj)
    fobj.close()

PATH = content["path"]

urlASM = "https://www.nseindia.com/reports/asm"
urlGSM = "https://www.nseindia.com/reports/gsm"

def fmt(li):
    newLi = []
    for i in li:
        st = i + ".NS"
        newLi.append(st)
    return newLi

def getGSM():
    pass

def getASMLong():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlASM)
        time.sleep(2.5)
        search = driver.find_element_by_id("asmLTTable")
        search = search.text
        li = search.split(" ")
        leng = len(li)

        count = 0

        if leng == 9:
            driver.quit()
            getASMLong()

        eg = "\n"

        while count < leng:
            i = li[count]
            if eg in i:
                asmLong.append(li[count + 1])
            count += 1

        asmLongFMT = fmt(asmLong)

        return asmLongFMT    
        
    except:
        getASMLong()

def getASMShort():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlASM)
        time.sleep(2.5)
        search = driver.find_element_by_id("asmSTTable")
        search = search.text
        li = search.split(" ")
        leng = len(li)

        count = 0

        if leng == 9:
            driver.quit()
            getASMLong()

        eg = "\n"

        while count < leng:
            i = li[count]
            if eg in i:
                asmShort.append(li[count + 1])
            count += 1

        asmShortFMT = fmt(asmShort)

        return asmShortFMT    
        
    except:
        getASMLong()

asmLong = getASMLong()
asmShort = getASMShort()
gms = getGSM()