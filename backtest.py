import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import ast
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

companies = ["AAPL","MSFT","AMZN","GOOGL","FB","NVDA","PYPL","NFLX","CMCSA","INTC","ADBE","AMD","TSM",
"PEP","CSCO","AVGO","QCOM","TMUS","COST","KO","TXN","AMGN","CHTR","SBUX","ABNB","AMAT","ISRG","MU","GILD"]

symbol = companies[5]

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

url = ("https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=Pkgha4QtRuo&lang=en-US&region=US&symbols=NVDA&fields=messageBoardId,longName,shortName,marketCap,underlyingSymbol,underlyingExchangeSymbol,headSymbolAsString,regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,uuid,regularMarketOpen,fiftyTwoWeekLow,fiftyTwoWeekHigh,toCurrency,fromCurrency,toExchange,fromExchange&corsDomain=finance.yahoo.com")
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text,"html.parser")

print(type(soup))

result = soup.string

with open("data.json","w") as fobj:
    json.dump(result,fobj)
    fobj.close()

with open("data.json","r") as fobj:
    content = json.load(fobj)

# print(content)
content = json.loads(content)
print(type(content))

print("52 Week High")
print(content["quoteResponse"]["result"][0]["fiftyTwoWeekHigh"]["fmt"])
