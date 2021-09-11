from bs4 import BeautifulSoup
import requests
import json

with open("NSE.json","r") as fobj:
    content = json.load(fobj)
    fobj.close()

for i in content:
    symbol = i

url = f"https://www.tickertape.in/stocks/itc-ITC?checklist=basic"

souce = requests.get(url)
