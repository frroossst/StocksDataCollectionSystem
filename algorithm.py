from matplotlib import pyplot as plt
from pandas_datareader import data
import pandas_datareader as pdr
import yfinance as yf
import pandas as pd
import numpy as np
import math
import json
import ta

# companies listed on the NASDAQ (USA)
with open("NASDAQ.json","r") as fobj:
    NASDAQ = json.load(fobj)
    fobj.close()

# NASDAQ = ["AAPL","MSFT","AMZN","GOOGL","FB","NVDA","PYPL","NFLX","CMCSA","INTC","ADBE","AMD","TSM",
# "PEP","CSCO","AVGO","QCOM","TMUS","COST","KO","TXN","AMGN","CHTR","SBUX","ABNB","AMAT","ISRG","MU","GILD"]

# companies listed on the NSE (India)
with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()


# NSE = ["ITC.NS","IOB.NS","MRPL.NS","IDEA.NS","SBIN.NS","INFY.NS","ASIANPAINT.NS","HCLTECH.NS","JUBLFOOD.NS","LT.NS","LTI.NS",
# "HINDUNILVR.NS","ONGC.NS","BAJFINANCE.NS","TATASTEEL.NS","TATAMOTORS.NS","TATACOFFEE.NS","TECHM.NS"]

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

def get_keltner_bands(symbol,dataF):
    dataF["KC middle"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_mband()
    dataF["KC low"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_lband()
    dataF["KC high"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_hband()

def get_bollinger_bands(symbol,dataF):
    # sma = get_sma(prices, rate)
    # std = prices.rolling(rate).std()
    # bollinger_up = sma + std * 2 # Calculate top band
    # bollinger_down = sma - std * 2 # Calculate bottom band
    # return bollinger_up, bollinger_down
    dataF["BB high"] = ta.volatility.BollingerBands(dataF["Close"], window=20,window_dev=2).bollinger_hband()
    dataF["BB low"] = ta.volatility.BollingerBands(dataF["Close"],window=20,window_dev=2).bollinger_lband()
    dataF["BB middle"] = ta.volatility.BollingerBands(dataF["Close"],window=20,window_dev=2).bollinger_mavg()


def get_momentum_squeeze(symbol,dataF):
    print("BB low",dataF["BB low"].iloc[-1])
    print("KC low",dataF["KC low"].iloc[-1])
    print("BB high",dataF["BB high"].iloc[-1])
    print("KC high",dataF["KC high"].iloc[-1])
    print("Close",dataF["Close"].iloc[-1])
    print("KC middle",dataF["KC middle"].iloc[-1])
    print("BB middle",dataF["BB middle"].iloc[-1])

    if dataF["BB high"].iloc[-1] > dataF["KC high"].iloc[-1] or dataF["BB low"].iloc[-1] < dataF["KC low"].iloc[-1] and (dataF["Close"].iloc[-1] >= dataF["KC middle"].iloc[-1]):
        if dataF["Close"].iloc[-2] > dataF["KC middle"].iloc[-1] and dataF["KC middle"].iloc[-1] > dataF["BB middle"].iloc[-1]:
            print("there is in an UPWARDS market trend")
            liMOMSQZE = "TRNDu"
        elif dataF["Close"].iloc[-2] < dataF["KC middle"].iloc[-1]:
            print("there is in a DOWNWARDS market trend")
            liMOMSQZE = "TRNDd"
        else: 
            print("the market is in a trend")
            liMOMSQZE = "TRND"
    elif dataF["BB low"].iloc[-1] > dataF["KC low"].iloc[-1] or dataF["BB high"].iloc[-1] < dataF["KC high"].iloc[-1] and (dataF["Close"].iloc[-1] <= dataF["KC middle"].iloc[-1]):
        print("market is in a SQUEEZE")
        liMOMSQZE = "SQZE"
    else:
        print("inconclusive")
        liMOMSQZE = "INCL"

    filename = symbol + ".json"

    try:
        with open(filename,"r") as fobj:
            content = json.load(fobj)
            fobj.close()

        content["Technical Indicators"].update({"MOMSQZE" : liMOMSQZE})

        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()
    except Exception as e:
        print(f"[{e}]")

def get_avg_volume(symbol,dataF,timeperiod=50):
    lastVol = dataF.iloc[-1]
    mod_dataF = dataF[:-1]

    mod_dataF = dataF["Volume"].tail(timeperiod)
    sumVol = mod_dataF.sum(axis=0, skipna=True)
    avgVol = sumVol/50

    if lastVol["Volume"] > avgVol:
        print("there is a VOLUME trend")
        print()
        volTrend = True

    else:
        print("there is NO volume trend")
        print()
        volTrend = False

    filename = symbol + ".json"

    try:
        with open(filename,"r") as fobj:
            content = json.load(fobj)
            fobj.close()

        content["Technical Indicators"].update({"50 day volume trend" : volTrend})

        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()
    except Exception as e:
        print(f"[{e}]")

def tenDayMA(symbol,dataF):
        mavg = get_sma(dataF["Close"],10)
        mavg = mavg.iloc[-1]
        filename = symbol + ".json"
        try:
            with open(filename,"r") as fobj:
                content = json.load(fobj)
                fobj.close()

            
            content["Technical Indicators"].update({"10 day MA" : mavg})

            with open(filename,"w") as fobj:
                json.dump(content,fobj,indent=6)
                fobj.close()
        
        except Exception as e:
            print(f"[{e}]")


def main(symbol):
    dataF = yf.Ticker(symbol).history(period="1y")
    get_keltner_bands(symbol,dataF)
    get_bollinger_bands(symbol,dataF)
    kc_middle, kc_high, kc_low = dataF["KC middle"], dataF["KC high"], dataF["KC low"]
    bb_up, bb_down= dataF["BB high"], dataF["BB low"]
    # print(dataF)
    print(symbol)
    get_momentum_squeeze(symbol,dataF)
    get_avg_volume(symbol,dataF)
    tenDayMA(symbol,dataF)
    # plt.title(symbol + ' Momentum Squeeze')
    # plt.style.use("seaborn")
    # plt.xlabel('Time Frame')
    # plt.ylabel('Closing Prices')
    # plt.plot(bb_up, label='Bollinger Up', c='k')
    # plt.plot(bb_down, label='Bollinger Down', c='k')
    # plt.plot(kc_middle,label="KC middle",c="b")
    # plt.plot(kc_high,label="KC high",c="b")
    # plt.plot(kc_low,label="KC low",c="b")
    # plt.legend()
    # plt.show()

for i in NSE:
    main(i)

# dataF = yf.Ticker(company).history(period="1y")
# get_avg_volume(dataF)