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
    
    dataF["KC middle"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20).keltner_channel_mband()
    dataF["KC low"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20).keltner_channel_lband()
    dataF["KC high"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20).keltner_channel_hband()
    

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down



symbol = NSE[0]
dataF = yf.Ticker(symbol).history(period="6mo")
print(dataF)
closing_prices = dataF["Close"]
bollinger_up, bollinger_down = get_bollinger_bands(closing_prices)
get_keltner_bands(dataF)
kc_middle, kc_high, kc_low = dataF["KC middle"], dataF["KC high"], dataF["KC low"]

plt.title(symbol + ' Momentum Squeeze')
plt.style.use("seaborn")
plt.xlabel('Time')
plt.ylabel('Closing Prices')
# plt.plot(closing_prices, label='Closing Prices')
plt.plot(bollinger_up, label='Bollinger Up', c='k')
plt.plot(bollinger_down, label='Bollinger Down', c='k')
plt.plot(kc_middle,label="KC middle",c="b")
plt.plot(kc_high,label="KC high",c="b")
plt.plot(kc_low,label="KC low",c="b")
# plt.fill_between(bollinger_up,bollinger_down,alpha=0.25,color="grey")
plt.legend()
plt.show()

