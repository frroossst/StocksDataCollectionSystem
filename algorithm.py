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
    atrVal = get_atr(dataF)
    atrValDF = pd.DataFrame(atrVal)
    atrSMA = get_sma(atrValDF,20)
    keltner_up = get_ema(dataF,20) + 2*atrSMA 
    keltner_down = get_ema(dataF,20) - 2*atrSMA
    keltner_middle = get_ema(dataF,20)
    return keltner_middle, keltner_up, keltner_down

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down



symbol = NASDAQ[5]
dataF = yf.Ticker(symbol).history(period="6mo")
print(dataF)
closing_prices = dataF["Close"]
bollinger_up, bollinger_down = get_bollinger_bands(closing_prices)
keltner_middle, keltner_up, keltner_down = get_keltner_bands(dataF)
get_ema(closing_prices,20)
get_atr(dataF)
print(f"BB = {bollinger_up,bollinger_down}")
print(f"KC = {keltner_middle, keltner_up,keltner_down}")
plt.title(symbol + ' Bollinger Bands')
plt.xlabel('Time')
plt.ylabel('Closing Prices')
plt.plot(closing_prices, label='Closing Prices')
plt.plot(bollinger_up, label='Bollinger Up', c='g')
plt.plot(bollinger_down, label='Bollinger Down', c='r')
plt.legend()
# plt.show()
