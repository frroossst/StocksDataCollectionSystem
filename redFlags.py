from bs4 import BeautifulSoup

import requests
import json

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

urlASM = "https://www.nseindia.com/reports/asm"
urlGSM = "https://www.nseindia.com/reports/gsm"

sourceASM = requests.get(urlASM, headers=headers).text
sourceGSM = requests.get(urlGSM, headers=headers).text

soupASM = BeautifulSoup(sourceASM,"lxml")
soupGMS = BeautifulSoup(sourceGSM,"lxml")

tableASMLong = soupASM.find("div", { "id" : "asm-lt-table-container"})
print(tableASMLong)

tableASMLong = soupASM.find("table",id = "asmLTTable")
tableASMShort = soupASM.find("table",id = "asmSTTable")


