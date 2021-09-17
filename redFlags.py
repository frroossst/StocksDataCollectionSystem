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

def getASM():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(urlASM)
        time.sleep(2.5)
        search = driver.find_element_by_id("asmLTTable")
        search = search.text
        li = search.split(" ")
        leng = len(li)

        count = 0

        print(li)

        if leng == 9:
            driver.quit()
            getASM()

        while count < leng:
            i = li[count]
            try:
                i = int(i)
                asmLong.append(li[count + 1])
                count += 2
            except:
                pass
            finally:
                count += 1

        print(asmLong)  
        driver.quit()    
    except:
        driver.quit()
        getASM()  
    
getASM()