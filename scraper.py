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

# companies listed on the NASDAQ (USA)
NASDAQ = ["AAPL","MSFT","AMZN","GOOGL","FB","NVDA","PYPL","NFLX","CMCSA","INTC","ADBE","AMD","TSM",
"PEP","CSCO","AVGO","QCOM","TMUS","COST","KO","TXN","AMGN","CHTR","SBUX","ABNB","AMAT","ISRG","MU","GILD"]

# companies listed on the NSE (India)
NSE = ["ITC.NS","IOB.NS","MRPL.NS","IDEA.NS","SBIN.NS","INFY.NS","ASIANPAINT.NS","HCLTECH.NS","JUBLFOOD.NS","LT.NS","LTI.NS",
"HINDUNILVR.NS","ONGC.NS","BAJFINANCE.NS","TATASTEEL.NS","TATAMOTORS.NS","TATACOFFEE.NS","TECHM.NS"]

#companies that are shooting up problems
li = ["GUJGAS.NS","SUNPHARMA.NS"]

global dump
dump = False

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

        global dump
        dump = True

        with open("data.json","r") as fobj:
            content = json.load(fobj)

        content = json.loads(content)

        try:
            ticker = (content["quoteResponse"]["result"][0]["symbol"])
            fiftyTwoWeekHigh = (content["quoteResponse"]["result"][0]["fiftyTwoWeekHigh"]["fmt"])
            fiftyTwoWeekLow = (content["quoteResponse"]["result"][0]["fiftyTwoWeekLow"]["fmt"])
            currentPrice = (content["quoteResponse"]["result"][0]["regularMarketPrice"]["fmt"])
            name = (content["quoteResponse"]["result"][0]["longName"])
            percentChange = (content["quoteResponse"]["result"][0]["regularMarketChangePercent"]["fmt"])
            dump = True
        except Exception as e:
            print("[{e}]")
            dump = False

        try:
            filename = ticker + ".json"
            dataDump = {
                "Basic Info" : {"Name" : name,"Symbol" : ticker, "Current Price" : currentPrice, "Change Percent" : percentChange, 
            "52 Week High" : fiftyTwoWeekHigh, "52 Week Low" : fiftyTwoWeekLow},
                "Technical Indicators" : {"RSI" : "", "ADX" : "","MACD" : ["",""],"OBV" : ""}
            }
        except Exception as e:
            print(f"[{e}]")
            dump = False

        if dump:
            with open(filename,"w") as fobj:
                json.dump(dataDump,fobj,indent=6)

    @classmethod
    def dumpData(self,ticker,data,type = None):
        
        if dump:

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
                data = round(data,4)
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
        
        else:
            print("dump attribute is false")


class technicalIndicators():

    def __init__(self) -> None:
        pass

    # method to get RSI
    def getRSI(self,ticker):
        self.ticker = ticker

        dataF = yf.Ticker(self.ticker).history(period="max").reset_index()[["Date","Close"]]
        dataF["RSI"] = ta.momentum.RSIIndicator(dataF["Close"], window = 14).rsi()
        lastDataF = dataF.iloc[-1]
        # print(lastDataF["RSI"])
        # print(type(dataF))
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

    # method to return ADX values
    def getADX(self,ticker):
        self.ticker = ticker

        self.ticker = ticker

        dataF = yf.download(self.ticker)

        dataF["ADX"] = talib.ADX(dataF["High"],dataF["Low"],dataF["Close"],timeperiod = 14)
        
        lastDataF = dataF.iloc[-1]
        data = lastDataF["ADX"]

        dataHandling.dumpData(self.ticker,data,"ADX")



### [FATAL] returns suspicious values
    def getOBV(self,ticker):
        self.ticker = ticker

        dataF = yf.download(self.ticker)
        dataF["OBV"] = talib.OBV(dataF["Close"],dataF["Volume"])

        lastDataF = dataF.iloc[-1]
        data = lastDataF["OBV"]
        dataHandling.dumpData(self.ticker,data,"OBV")



def main():

    exchange = input("enter exchange to scrape : ")

    if exchange == "nasdaq":
        for i in NASDAQ:
            i = i + ".json"
            if os.path.exists(i):
                os.remove(i)

        print("collecting data...")
        for i in NASDAQ:
            symbol = i
            D = dataHandling()
            D.getData(symbol)
            T = technicalIndicators()
            T.getRSI(symbol)
            T.getMACD(symbol)
            T.getADX(symbol)
            T.getOBV(symbol)

    elif exchange == "nse":
        for i in NSE:
            i = i + ".json"
            if os.path.exists(i):
                os.remove(i)

        print("collecting data...")
        for i in NSE:
            symbol = i
            D = dataHandling()
            D.getData(symbol)
            T = technicalIndicators()
            T.getRSI(symbol)
            T.getMACD(symbol)
            T.getADX(symbol)
            T.getOBV(symbol)


main()



