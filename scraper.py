from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from matplotlib import pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import talib
import json
import csv
import os
import ta



# companies listed on the NASDAQ (USA)

try:
    with open("NASDAQ.json","r") as fobj:
        NASDAQ = json.load(fobj)
        fobj.close()
except Exception as e:
    print(f"[{e}]")

# companies listed on the NSE (India)

with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()

#companies that are shooting up problems
li = ["GUJGAS.NS","SUNPHARMA.NS"]

global dump
dump = False

class dataHandling():

    def __init__(self) -> None:
        result = ""
        
    @classmethod
    def reNSE(self,symbol):
        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}
        urlNSEpercen = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}&section=trade_info"
        rNSE = requests.get(urlNSEpercen)
        soup = BeautifulSoup(rNSE.text,"html.parser")
        result = soup.string
        return result

    def getData(self,symbol):

        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

        url = (f"https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=Pkgha4QtRuo&lang=en-US&region=US&symbols={symbol}&fields=messageBoardId,longName,shortName,marketCap,underlyingSymbol,underlyingExchangeSymbol,headSymbolAsString,regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,uuid,regularMarketOpen,fiftyTwoWeekLow,fiftyTwoWeekHigh,toCurrency,fromCurrency,toExchange,fromExchange&corsDomain=finance.yahoo.com")
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text,"html.parser")
        result = soup.string

        newSymbol = ""

        for i in symbol:
            if i != ".":
                newSymbol += i
            else:
                break

        # # result returns None
        urlNSEpercen = f"https://www.nseindia.com/api/quote-equity?symbol={newSymbol}&section=trade_info"
        rNSE = requests.get(urlNSEpercen,headers=headers)
        if rNSE.status_code == 401:
            print(f"[401] Website denies auth for {newSymbol}")
            authDeliv = False # delivPercen will not be retrieved
        else:
            print(f"[OK] Fetching delivery percentage for {newSymbol}")
            authDeliv = True # delivPercen will be retrieved

        if authDeliv:

            soup = BeautifulSoup(rNSE.text, "html.parser")
            data = soup.prettify()
            try:
                data = json.loads(data)
            except Exception as e:
                print(f"[{e}]")
                quit()

        else:
            pass

        if authDeliv:
            try:
                delivPercen = ((int(data["securityWiseDP"]["quantityTraded"]) - int(data["securityWiseDP"]["deliveryQuantity"])) / int(data["securityWiseDP"]["quantityTraded"])) * 100
                delivPercen = str(round(delivPercen,2)) + "%"
            except ZeroDivisionError:
                delivPercen = "0.0%"
        # print(delivPercen)

        result = json.loads(result)
 
        if authDeliv:
            result["quoteResponse"]["result"][0]["delivPercen"] = delivPercen
        # print(result)

        with open("data.json","w") as fobj:
            json.dump(result,fobj,indent=6)
            fobj.close()

        dataHandling.getAttributes(self,authDeliv)

    def getAttributes(self,authDeliv):

        global dump
        dump = True

        with open("data.json","r") as fobj:
            content = json.load(fobj)

        # content = json.loads(content)

        # delivPercen = "%" + "of Deliverable Quantity to Traded Quantity"

        try:
            ticker = (content["quoteResponse"]["result"][0]["symbol"])
            fiftyTwoWeekHigh = (content["quoteResponse"]["result"][0]["fiftyTwoWeekHigh"]["fmt"])
            fiftyTwoWeekLow = (content["quoteResponse"]["result"][0]["fiftyTwoWeekLow"]["fmt"])
            currentPrice = (content["quoteResponse"]["result"][0]["regularMarketPrice"]["fmt"])
            name = (content["quoteResponse"]["result"][0]["longName"])
            percentChange = (content["quoteResponse"]["result"][0]["regularMarketChangePercent"]["fmt"])
            if authDeliv:
                delivPercen = (content["quoteResponse"]["result"][0]["delivPercen"])
            dump = True
        except Exception as e:
            print(f"[{e}]")
            dump = False

        try:
            filename = ticker + ".json"
            if authDeliv == False:
                delivPercen = "NA"
            dataDump = {
                "Basic Info" : {"Name" : name,"Symbol" : ticker, "Current Price" : currentPrice, "Change Percent" : percentChange, 
            "52 Week High" : fiftyTwoWeekHigh, "52 Week Low" : fiftyTwoWeekLow, "Deliverable to Traded Quantity Percent" : delivPercen},
                "Technical Indicators" : {"RSI" : "", "ADX" : "","MACD" : ["",""],"OBV" : "","MFI" : "","50 day volume trend" : "","MOMSQZE" : "", "10 day MA" : ""}
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
            
            elif type == "MFI":
                data = round(data,4)
                content["Technical Indicators"].update({"MFI" : data})

            elif type == "AVGVOL":
                data = round(data,4)
                content["Technical Indicators"].update({"50 day volume trend" : data})

            else:
                raise Exception("type None is not a valid keyword input")

            with open(filename,"w") as fobj:
                json.dump(content,fobj,indent=6)
                fobj.close()
        
        else:
            print("dump attribute is false")

    def saveData(self,ticker):

        filename = ticker + ".csv"
        with open(filename,"r") as fobj:
            content = csv.reader(fobj)
            fobj.close()

        data = yf.Ticker(ticker).history(period="1y")
        dataC = data.to_csv()
        content["rawData"] = dataC
        
        with open(filename,"w") as fobj:
            csv.writer(dataC)
            fobj.close()

class technicalIndicators():

    def __init__(self) -> None:
        pass

    # method to get RSI
    def getRSI(self,ticker,data):
        self.ticker = ticker
        
        dataF = data.reset_index()[["Date","Close"]]
        dataF["RSI"] = ta.momentum.RSIIndicator(dataF["Close"], window = 14).rsi()
        lastDataF = dataF.iloc[-1]
        # print(lastDataF["RSI"])
        # print(type(dataF))
        dataHandling.dumpData(self.ticker,lastDataF["RSI"],"RSI")

    # method to get MACD
    def getMACD(self,ticker,data):
        self.ticker = ticker
        dataF = data

        dataF["MACD Line"] = ta.trend.MACD(dataF["Close"],window_slow = 26, window_fast = 12, window_sign = 9).macd()
        dataF["MACD Signal"] = ta.trend.MACD(dataF["Close"],window_slow = 26, window_fast = 12, window_sign = 9).macd_signal()

        lastDataF = dataF.iloc[-1]
        data = [lastDataF["MACD Line"], lastDataF["MACD Signal"]]

        dataHandling.dumpData(self.ticker,data,"MACD")

    # method to return ADX values
    def getADX(self,ticker,data):
        self.ticker = ticker

        self.ticker = ticker
        dataF = data

        dataF["ADX"] = talib.ADX(dataF["High"],dataF["Low"],dataF["Close"],timeperiod = 14)
        
        lastDataF = dataF.iloc[-1]
        data = lastDataF["ADX"]

        dataHandling.dumpData(self.ticker,data,"ADX")

    def getMFI(self,ticker,data):
        self.ticker = ticker
        dataF = data

        dataF["MFI"] = talib.MFI(dataF["High"],dataF["Low"],dataF["Close"],dataF["Volume"],timeperiod=14)

        lastDataF = dataF.iloc[-1]
        data = lastDataF["MFI"]
        dataHandling.dumpData(self.ticker,data,"MFI") 

### [FATAL] returns suspicious values
    def getOBV(self,ticker,data):
        self.ticker = ticker
        dataF = data

        dataF["OBV"] = talib.OBV(dataF["Close"],dataF["Volume"])

        lastDataF = dataF.iloc[-1]
        data = lastDataF["OBV"]
        dataHandling.dumpData(self.ticker,data,"OBV")

    # def get_avg_volume(self,ticker,timeperiod=50):
    #     self.ticker = ticker

    #     dataF = yf.Ticker(self.ticker).history(period="1y")
    #     dataF_vol = dataF["Volume"].tail(timeperiod)
    #     sumVol = dataF_vol.sum(axis=0, skipna=True)
    #     lastVol = dataF.iloc[-1]

    #     if lastVol["Volume"] > sumVol:
    #         print("There is a volume trend")
    #         volTrend = True
    #     else:
    #         print("There is no particular trend")
    #         volTrend = False

    #     dataHandling.dumpData(self.ticker,volTrend,"AVGVOL")



def main(exch="ind",auto=True):

    if not auto:
        print("1. Scrape Data")
        print("2. Add a company")
        # print("3. Remove a company")
        ch = int(input("enter choice : "))

    elif auto:
        ch = 1
        with open("settings.json","r") as fobj:
            content = json.load(fobj)
            fobj.close()
        exchange = content["exchg"]

    else:
        raise ValueError ("value not found for auto")

    if ch == 1:
        if not auto:
            exchange = input("enter exchange to scrape : ")

        if exchange == "usa" or exchange == "nasdaq":
            for i in NASDAQ:
                i = i + ".json"
                if os.path.exists(i):
                    os.remove(i)

            # print("collecting data...")
            for i in NASDAQ:
                symbol = i
                D = dataHandling()
                D.getData(symbol)
                T = technicalIndicators()
                dataF = yf.download(symbol)
                T.getRSI(symbol,dataF)
                T.getMACD(symbol,dataF)
                T.getADX(symbol,dataF)
                T.getOBV(symbol,dataF)
                T.getMFI(symbol,dataF)
                # T.get_avg_volume(symbol)

        elif exchange == "ind" or exchange == "nse":
            if not auto:
                for i in NSE:
                    i = i + ".json"
                    if os.path.exists(i):
                        os.remove(i)

            # print("collecting data...")
            for i in NSE:
                symbol = i
                D = dataHandling()
                D.getData(symbol)
                T = technicalIndicators()
                dataF = yf.download(symbol)
                T.getRSI(symbol,dataF)
                T.getMACD(symbol,dataF)
                T.getADX(symbol,dataF)
                T.getOBV(symbol,dataF)
                T.getMFI(symbol,dataF)
                # D.saveData(symbol)
                # T.get_avg_volume(symbol)

    elif ch == 2:

        exchange = input("enter exchange to scrape : ")

        if exchange == "usa" or exchange == "nasdaq":
            print(f"Companies List : {NASDAQ}")
            fmtTicker = "For examples : NVIDIA Corp => NVDA"
            print(fmtTicker)
            compAdd = input("enter ticker : ")
            NASDAQ.append(compAdd)
            with open("NASDAQ.json","w") as fobj:
                json.dump(NASDAQ,fobj,indent=6)
                fobj.close()

        elif exchange == "ind" or exchange == "nse":
            print(f"Companies List : {NSE}")
            fmtTicker = "For examples : ITC => ITC.NS"
            print(fmtTicker)
            compAdd = input("enter ticker : ")
            NSE.append(compAdd)
            with open("NSE.json","w") as fobj:
                json.dump(NSE,fobj,indent=6)
                fobj.close()

    elif ch == 3:

        exchange = input("enter exchange to scrape : ")

        if exchange == "usa" or exchange == "nasdaq":
            print(f"Companies List : {NASDAQ}")
            fmtTicker = "For examples : NVIDIA Corp => NVDA"
            print(fmtTicker)
            compRem = input("enter ticker : ")
            NASDAQ.remove(compRem)

        elif exchange == "ind" or exchange == "nse":
            print(f"Companies List : {NSE}")
            fmtTicker = "For examples : ITC => ITC.NS"
            print(fmtTicker)
            compRem = input("enter ticker : ")
            NSE.remove(compRem)


main(auto=True)



