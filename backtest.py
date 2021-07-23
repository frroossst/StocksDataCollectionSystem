import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import os
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



class dataHandling():

    def __init__(self) -> None:
        result = ""
        
    def getData(self,symbol):

        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

        url = (f"https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=Pkgha4QtRuo&lang=en-US&region=US&symbols={symbol}&fields=messageBoardId,longName,shortName,marketCap,underlyingSymbol,underlyingExchangeSymbol,headSymbolAsString,regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,uuid,regularMarketOpen,fiftyTwoWeekLow,fiftyTwoWeekHigh,toCurrency,fromCurrency,toExchange,fromExchange&corsDomain=finance.yahoo.com")
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text,"html.parser")
        result = soup.string

        with open("data.json","w") as fobj:
            json.dump(result,fobj)
            fobj.close()

        dataHandling.getAttributes(self)

    def getAttributes(self):

        with open("data.json","r") as fobj:
            content = json.load(fobj)

        content = json.loads(content)

        ticker = (content["quoteResponse"]["result"][0]["symbol"])
        fiftyTwoWeekHigh = (content["quoteResponse"]["result"][0]["fiftyTwoWeekHigh"]["fmt"])
        fiftyTwoWeekLow = (content["quoteResponse"]["result"][0]["fiftyTwoWeekLow"]["fmt"])
        currentPrice = (content["quoteResponse"]["result"][0]["regularMarketPrice"]["fmt"])
        name = (content["quoteResponse"]["result"][0]["longName"])

        filename = ticker + ".json"
        dataDump = {"Name" : name,"Symbol" : ticker, "Current Price" : currentPrice,"52 Week High" : fiftyTwoWeekHigh,"52 Week Low" : fiftyTwoWeekLow}

        with open(filename,"w") as fobj:
            json.dump(dataDump,fobj,indent=6)

def main():

    for i in companies:
        i = i + ".json"
        if os.path.exists(i):
            os.remove(i)

    for i in companies:
        symbol = i
        D = dataHandling()
        D.getData(symbol)

main()