import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import time
import requests
from bs4 import BeautifulSoup


# # # Basic Stocks Trading Strategy

# # # [BUY]
# # # 1. 26 week high is greater than 52 week high
# # # 2. RSI > 70 
# # # 3. ADX > 25
# # # 4. MACD signal is true
# # # 5. 50 day EMA is greater than 200 day EMA
# # # 6. OBV signal is up!

# # # [SELL]
# # # 1. 26 week average is less than 52 week high
# # # 2. RSI > 75
# # # 3. ADX > 25
# # # 4. MACD is set to sell
# # # 5. current price is 0.70 * bought price

# BS4 method

companies = ["AAPL","MSFT","AMZN","GOOGL","FB","NVDA","PYPL","NFLX","CMCSA","INTC","ADBE","AMD","TSM",
"PEP","CSCO","AVGO","QCOM","TMUS","COST","KO","TXN","AMGN","CHTR","SBUX","ABNB","AMAT","ISRG","MU","GILD"]

symbol = companies[5]

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}
# url = f"https://finance.yahoo.com/quote/{symbol}"
# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.text,"html.parser")
# print(symbol)
# currentPrice = soup.find("span",{"class" : "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
# print(currentPrice)

url = "https://finance.yahoo.com/quote/NVDA/key-statistics?p=NVDA"
r = requests.get(url, headers= headers)
soup = BeautifulSoup(r.text,"html.parser")

# print(symbol)
# fiftyTwoWeekHigh = soup.find_all("td",{"class" : "Fw(500) Ta(end) Pstart(10px) Miw(60px)"})
# print(fiftyTwoWeekHigh)

textWall = soup.get_text()
print(textWall)
fiftyWeekHigh = "52 Week High 3"
lindex = 0
compar = []

for i in textWall:
    compar.append(i)
    if "".join(compar) == fiftyWeekHigh:
        print("found a match")
    elif len(compar) > 14:
        compar = []
    else:
        pass





