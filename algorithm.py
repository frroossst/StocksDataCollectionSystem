from matplotlib import pyplot as plt
from pandas_datareader import data
import pandas_datareader as pdr
import yfinance as yf
import pandas as pd
import numpy as np
import talib
import math
import json
import os
import ta

# companies listed on the NASDAQ (USA)
NASDAQ = ["AAPL","MSFT","AMZN","GOOGL","FB","NVDA","PYPL","NFLX","CMCSA","INTC","ADBE","AMD","TSM",
"PEP","CSCO","AVGO","QCOM","TMUS","COST","KO","TXN","AMGN","CHTR","SBUX","ABNB","AMAT","ISRG","MU","GILD"]

# companies listed on the NSE (India)
NSE = ["ITC.NS","IOB.NS","MRPL.NS","IDEA.NS","SBIN.NS","INFY.NS","ASIANPAINT.NS","HCLTECH.NS","JUBLFOOD.NS","LT.NS","LTI.NS",
"HINDUNILVR.NS","ONGC.NS","BAJFINANCE.NS","TATASTEEL.NS","TATAMOTORS.NS","TATACOFFEE.NS","TECHM.NS"]

#companies that are shooting up problems
li = ["GUJGAS.NS","SUNPHARMA.NS"]

def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_ema(prices, rate):
    return prices.ewm(span=20,adjust=False).mean()

def get_atr(dataF):
    lengthDataF = dataF.shape[0]
    atrLi = []
    startLoc = 1
    while startLoc < lengthDataF:
        todayRow = dataF.iloc[startLoc]
        yesterdayRow = dataF.iloc[startLoc -1]
        tr0 = math.fabs(todayRow["High"] - todayRow["Low"]) # today's high - today's low
        tr1 = math.fabs(todayRow["High"] - yesterdayRow["Close"]) # today's high - yesterday's close
        tr2 = math.fabs(yesterdayRow["Close"] - todayRow["Low"]) # yesterday's close - today's low 
        atrLi.append(max(tr0,tr1,tr2))
        startLoc += 1
    return atrLi

def get_keltner_bands(dataF):
    dataF["KC middle"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_mband()
    dataF["KC low"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_lband()
    dataF["KC high"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_hband()

def get_bollinger_bands(dataF):
    # sma = get_sma(prices, rate)
    # std = prices.rolling(rate).std()
    # bollinger_up = sma + std * 2 # Calculate top band
    # bollinger_down = sma - std * 2 # Calculate bottom band
    # return bollinger_up, bollinger_down
    print(dataF)
    dataF["BB high"] = ta.volatility.BollingerBands(dataF["Close"], window=20,window_dev=2).bollinger_hband()
    dataF["BB low"] = ta.volatility.BollingerBands(dataF["Close"],window=20,window_dev=2).bollinger_lband()

def get_momentum_squeeze(symbol,dataF):
    print("BB low",dataF["BB low"].iloc[-1])
    print("KC low",dataF["KC low"].iloc[-1])
    print("BB high",dataF["BB high"].iloc[-1])
    print("KC high",dataF["KC high"].iloc[-1])
    print("Close",dataF["Close"].iloc[-1])
    print("KC middle",dataF["KC middle"].iloc[-1])

    if dataF["BB high"].iloc[-1] > dataF["KC high"].iloc[-1] or dataF["BB low"].iloc[-1] < dataF["KC low"].iloc[-1] and (dataF["Close"].iloc[-1] >= dataF["KC middle"].iloc[-1]):
        print("market is in a trend")
        liMOMSQZE = "TRND"
    elif dataF["BB low"].iloc[-1] > dataF["KC low"].iloc[-1] or dataF["BB high"].iloc[-1] < dataF["KC high"].iloc[-1] and (dataF["Close"].iloc[-1] <= dataF["KC middle"].iloc[-1]):
        print("market is in a squeeze")
        liMOMSQZE = "SQZE"
    else:
        print("inconclusive")
        liMOMSQZE = "INCL"

    filename = symbol + ".json"

    with open(filename,"r") as fobj:
        content = json.load(fobj)
        fobj.close()

    content["Technical Indicators"].update({"MOMSQZE" : liMOMSQZE})

    with open(filename,"w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()

def get_avg_volume(symbol,dataF,timeperiod=50):
    dataF_vol = dataF["Volume"].tail(timeperiod)
    sumVol = dataF_vol.sum(axis=0, skipna=True)
    lastVol = dataF.iloc[-1]

    if lastVol["Volume"] > sumVol:
        print("There is a volume trend")
        volTrend = True

    else:
        print("There is no particular trend")
        volTrend = False

    filename = symbol + ".json"

    with open(filename,"r") as fobj:
        content = json.load(fobj)
        fobj.close()

    content["Technical Indicators"].update({"50 day volume trend" : volTrend})

    with open(filename,"w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()



def main(symbol):
    dataF = yf.Ticker(symbol).history(period="1y")
    closing_prices = dataF["Close"]
    get_keltner_bands(symbol,dataF)
    get_bollinger_bands(symbol,dataF)
    kc_middle, kc_high, kc_low = dataF["KC middle"], dataF["KC high"], dataF["KC low"]
    bb_up, bb_down= dataF["BB high"], dataF["BB low"]
    print(dataF)
    get_momentum_squeeze(symbol,dataF)
    get_avg_volume(symbol,dataF,symbol)
    plt.title(symbol + ' Momentum Squeeze')
    plt.style.use("seaborn")
    plt.xlabel('Time Frame')
    plt.ylabel('Closing Prices')
    plt.plot(bb_up, label='Bollinger Up', c='k')
    plt.plot(bb_down, label='Bollinger Down', c='k')
    plt.plot(kc_middle,label="KC middle",c="b")
    plt.plot(kc_high,label="KC high",c="b")
    plt.plot(kc_low,label="KC low",c="b")
    plt.legend()
    plt.show()



company = NSE[0]
main(company)

# dataF = yf.Ticker(company).history(period="1y")
# get_avg_volume(dataF)