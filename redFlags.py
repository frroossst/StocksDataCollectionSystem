from bs4 import BeautifulSoup
import bs4 as bs
import requests
import json

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

urlASM = "https://www.nseindia.com/reports/asm"
urlGSM = "https://www.nseindia.com/reports/gsm"

sourceASM = requests.get(urlASM, headers=headers).text
sourceGSM = requests.get(urlGSM, headers=headers).text

soupASM = bs.BeautifulSoup(sourceASM,"lxml")
soupGMS = bs.BeautifulSoup(sourceGSM,"lxml")

print(soupASM)