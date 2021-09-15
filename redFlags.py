from bs4 import BeautifulSoup
import requests
import json

urlASM = "https://www.nseindia.com/reports/asm/"
urlGSM = "https://www.nseindia.com/reports/gsm/"

sourceASM = requests.get("https://www.nseindia.com/reports/asm/").text
sourceGSM = requests.get(urlGSM).text

soupASM = BeautifulSoup(sourceASM,"lxml")
soupGMS = BeautifulSoup(sourceGSM,"lxml")

print(soupASM.prettify())

tableASM = soupASM.find("table",id = "asmLTTable")
print(tableASM)
