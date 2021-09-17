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

driver = webdriver.Chrome(PATH)
driver.get(urlASM)
time.sleep(1.5)
search = driver.find_element_by_id("asmLTTable")
search = search.text
li = search.split(" ")
leng = len(li)

count = 0
while count < leng:
    print(li[count])
    try:
        print(type(li[count]))
        print(int(li[count]))
        if int(li[count]).isnum():
            asmLong.append(li[count +1])
        else:
            count += 1
    except:
        count += 1
        continue

print(asmLong)