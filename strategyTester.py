from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import json
import math
import ta

class method():
    
    @classmethod
    def getData(self,symbol):
        # filename = symbol + ".csv"
        dataF = yf.Ticker(symbol).history(period="max")
        return dataF

    @classmethod
    def loadScrips(self):
        with open("NSE.json","r") as fobj:
            NSE = json.load(fobj)
            fobj.close()
        return NSE


class technical():

    def __init__(self) -> None:
        pass

    def get_keltner_bands(self,symbol,dataF):
        dataF["KC middle"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_mband()
        dataF["KC low"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_lband()
        dataF["KC high"] = ta.volatility.KeltnerChannel(dataF["High"],dataF["Low"],dataF["Close"],window=20,window_atr=10,original_version=False).keltner_channel_hband()

    def get_bollinger_bands(self,symbol,dataF):
        dataF["BB high"] = ta.volatility.BollingerBands(dataF["Close"], window=20,window_dev=2).bollinger_hband()
        dataF["BB low"] = ta.volatility.BollingerBands(dataF["Close"],window=20,window_dev=2).bollinger_lband()
        dataF["BB middle"] = ta.volatility.BollingerBands(dataF["Close"],window=20,window_dev=2).bollinger_mavg()

    def get_momentum_squeeze(self,symbol,dataF):
        limomsqze = []
        limomsqze += 52 * [np.nan] 
        iterVar = 52
        while True:
            try:
                if dataF["BB high"].iloc[iterVar] > dataF["KC high"].iloc[iterVar] or dataF["BB low"].iloc[iterVar] < dataF["KC low"].iloc[iterVar] and (dataF["Close"].iloc[iterVar] >= dataF["KC middle"].iloc[iterVar]):
                    if dataF["Close"].iloc[iterVar - 1] > dataF["KC middle"].iloc[iterVar] and dataF["KC middle"].iloc[iterVar] > dataF["BB middle"].iloc[iterVar]:
                        # print("there is in an UPWARDS market trend")
                        MOMSQZE = "TRNDu"
                    elif dataF["Close"].iloc[iterVar - 1] < dataF["KC middle"].iloc[iterVar]:
                        # print("there is in a DOWNWARDS market trend")
                        MOMSQZE = "TRNDd"
                    else: 
                        # print("the market is in a trend")
                        MOMSQZE = "TRND"
                elif dataF["BB low"].iloc[iterVar] > dataF["KC low"].iloc[iterVar] or dataF["BB high"].iloc[iterVar] < dataF["KC high"].iloc[iterVar] and (dataF["Close"].iloc[iterVar] <= dataF["KC middle"].iloc[iterVar]):
                    # print("market is in a SQUEEZE")
                    MOMSQZE = "SQZE"
                else:
                    # print("inconclusive")
                    MOMSQZE = "INCL"
                # print(MOMSQZE)
                limomsqze.append(MOMSQZE)
                iterVar += 1
            except:
                break
        dataF["MOMSQZE"] = limomsqze

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



T = technical()
scrips = method.loadScrips()
for i in scrips:   
    dataF = method.getData(i)
    T.get_keltner_bands(i,dataF)
    T.get_bollinger_bands(i,dataF)
    T.get_momentum_squeeze(i,dataF)
    print(dataF)
    break