from pandas.core.window.rolling import Window
import yfinance as yf
import pandas as pd
import ta
import talib
import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
import json
import os
import math


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
        percentChange = (content["quoteResponse"]["result"][0]["regularMarketChangePercent"]["fmt"])

        filename = ticker + ".json"
        dataDump = {
            "Basic Info" : {"Name" : name,"Symbol" : ticker, "Current Price" : currentPrice, "Change Percent" : percentChange, 
        "52 Week High" : fiftyTwoWeekHigh, "52 Week Low" : fiftyTwoWeekLow},
            "Technical Indicators" : {"RSI" : "", "ADX" : "","MACD" : ["",""],"OBV" : ""}
        }

        with open(filename,"w") as fobj:
            json.dump(dataDump,fobj,indent=6)

    @classmethod
    def dumpData(self,ticker,data,type = None):
        
        filename = ticker + ".json"
        
        with open(filename,"r") as fobj:
            content = json.load(fobj)
            fobj.close()

        if type == "RSI":
            data = round(data,4)
            content["Technical Indicators"].update({"RSI" : data})

        elif type == "OBV":
            content["Technical Indicators"].update({"OBV" : data})

        elif type == "ADX":
            content["Technical Indicators"].update({"ADX" : data})

        elif type == "MACD":
            # data input is a list for MACD
            data = [round(data[0],4), round(data[1],4)]
            content["Technical Indicators"].update({"MACD" : [{"Line" : data[0]}, {"Signal" : data[1]}]})
        else:
            raise Exception("type None is not a valid keyword input")

        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()


class technicalIndicators():

    def __init__(self) -> None:
        pass

    # method to get RSI
    def getRSI(self,ticker):
        self.ticker = ticker

        dataF = yf.Ticker(self.ticker).history(period="max").reset_index()[["Date","Close"]]
        dataF["RSI"] = ta.momentum.RSIIndicator(dataF["Close"], window = 14).rsi()
        lastDataF = dataF.iloc[-1]
        print(lastDataF["RSI"])
        print(type(dataF))
        dataHandling.dumpData(self.ticker,lastDataF["RSI"],"RSI")

    # method to get MACD
    def getMACD(self,ticker):
        self.ticker = ticker

        dataF = yf.download(self.ticker)

        dataF["MACD Line"] = ta.trend.MACD(dataF["Close"],window_slow = 26, window_fast = 12, window_sign = 9).macd()
        dataF["MACD Signal"] = ta.trend.MACD(dataF["Close"],window_slow = 26, window_fast = 12, window_sign = 9).macd_signal()

        lastDataF = dataF.iloc[-1]
        data = [lastDataF["MACD Line"], lastDataF["MACD Signal"]]

        dataHandling.dumpData(self.ticker,data,"MACD")

### [FATAL] return NaN
    def getADX(self,ticker):
        self.ticker = ticker

        dataF = yf.download(self.ticker)
        print(dataF)
        dataF["ADX"] = ta.trend.ADXIndicator(dataF["High"].values,dataF["Low"].values,dataF["Close"].values,window=14).adx()
        lastDataF = dataF.iloc[-1]
        print(lastDataF["ADX"])

        adx = talib.ADX(dataF["High"].values,dataF["Low"].values,dataF["Close"].values)
        print(adx)

        #dataHandling.dumpData(self.ticker,adx,"ADX")

    def getOBV(self,ticker):
        self.ticker = ticker

        dataF = yf.download(self.ticker)
        #not sure this is accurate!
        dataF["OBV"] = ta.volume.OnBalanceVolumeIndicator(dataF["Close"],dataF["Volume"]).on_balance_volume()
        print(dataF["OBV"])
        lastDataF = dataF.iloc[-1]
        print(lastDataF["OBV"])

    


def main():

    for i in companies:
        i = i + ".json"
        if os.path.exists(i):
            os.remove(i)

    for i in companies:
        symbol = i
        D = dataHandling()
        D.getData(symbol)

# main()

symbol = companies[5]
D = dataHandling()
D.getData(symbol)
T = technicalIndicators()
T.getOBV("NVDA")