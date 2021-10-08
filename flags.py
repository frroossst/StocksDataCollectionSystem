from selenium import webdriver
import json
import time

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

# global asmShortCounter
# global asmLongCounter
# global gsmCounter
# asmShortCounter = 0
# asmLongCounter = 0
# gsmCounter = 0

redflagsFMT = {
    "asmShort" : [],
    "asmLong" : [],
    "gsm" : []
}

asmShort = []
asmLong = []
gsm = []

with open("settings.json","r") as fobj:
    content = json.load(fobj)
    fobj.close()

PATH = content["path"]
waitPeriod = content["chromiumWait"]

urlASM = "https://www.nseindia.com/reports/asm"
urlGSM = "https://www.nseindia.com/reports/gsm"

def fmt(li):
    newLi = []
    for i in li:
        st = i + ".NS"
        newLi.append(st)
    return newLi

def getASMLong():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlASM)
        time.sleep(waitPeriod)
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

        driver.quit()
        asmLongFMT = fmt(asmLong)
        print("[OK] ASM Long Term")
        return asmLongFMT    
        
    except Exception as e:
        driver.quit()
        getASMLong()

def getASMShort():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlASM)
        time.sleep(waitPeriod)
        search = driver.find_element_by_id("asmSTTable")
        search = search.text
        li = search.split(" ")
        leng = len(li)

        count = 0

        eg = "\n"

        while count < leng:
            i = li[count]
            if eg in i:
                asmShort.append(li[count + 1])
            count += 1

        driver.quit()
        asmShortFMT = fmt(asmShort)
        print("[OK] ASM Short Term")
        return asmShortFMT    
        
    except:
        driver.quit()
        getASMShort()

def getGSM():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlGSM)
        time.sleep(2.5)
        search = driver.find_element_by_id("gsmTable")
        search = search.text
        li = search.split(" ")
        leng = len(li)

        count = 0

        eg = "\n"

        while count < leng:
            i = li[count]
            if eg in i:
                gsm.append(li[count + 1])
            count += 1

        driver.quit()
        gsmFMT = fmt(gsm)
        print("[OK] GSM")
        return gsmFMT    
        
    except:
        driver.quit()
        getGSM()

def checkNone():
    isChange = False
    with open("redflags.json","r") as fobj:
        content = json.load(fobj)
        if content["asmShort"] == None:
            print("[ERROR] asmShort is None")
            asmShort = getASMShort()
            redflagsFMT["asmShort"] = asmShort
            isChange = True
        if content["asmLong"] == None:
            print("[ERROR] asmLong is None")
            asmLong = getASMLong()
            redflagsFMT["asmLong"] = asmLong
            isChange = True
        if content["gsm"] == None:
            print("[ERROR] gsm is None")
            gsm = getGSM()
            redflagsFMT["gsm"] = gsm
            isChange = True
        
        if isChange:
            with open("redflags.json","w") as fobj:
                json.dump(redflagsFMT,fobj,indent=6)
                fobj.close()



try:
    asmLong = getASMLong()
    asmShort = getASMShort()
    gsm = getGSM()
except Exception as e:
    print(f"[ERRPR] {e}")

redflagsFMT["asmShort"] = asmShort
redflagsFMT["asmLong"] = asmLong
redflagsFMT["gsm"] = gsm

with open("redflags.json","w") as fobj:
    json.dump(redflagsFMT,fobj,indent=6)
    fobj.close()

checkNone()