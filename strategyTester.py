from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd
import numpy as np
import json
import math
import time
import ta

class method():
    
    @classmethod
    def getData(self,symbol) -> DataFrame:
        # filename = symbol + ".csv"
        dataF = yf.Ticker(symbol).history(period="max")
        return dataF

    @classmethod
    def loadScrips(self):
        with open("NSE.json","r") as fobj:
            NSE = json.load(fobj)
            fobj.close()
        return NSE

    @classmethod
    def dumpData(self,symbol,dataF):
        filename = symbol + ".csv"
        dataF.to_csv(filename)



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
        limomsqze += 20 * [np.nan] 
        iterVar = 20
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

    def get_avg_volume(self,symbol,dataF):
        
        dataF["vol_avg"] = dataF["Volume"].rolling(50).mean() 

    def get_10day_ma(self,symbol,dataF):

        dataF["10_ma"] = dataF["Close"].rolling(10).mean()



class strategy():

    # Add custom function to test your strategy

    def __init__(self) -> None:
        pass

    def simulateBuy(self,symbol,date,price):
        filename = symbol + ".trade"
        
        try:
            with open(filename,"r") as fobj:
                content = json.load(fobj)
                fobj.close()
        except:
            dictFMT = {"Stats" : {},"BUY" : {}, "SELL" : {}}
            with open(filename,"w") as fobj:
                json.dump(dictFMT,fobj,indent=6)
                fobj.close()
            with open(filename,"r") as fobj:
                content = json.load(fobj)
                fobj.close()

        content["BUY"][date] = round(price,2)

        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()

    def simulateSell(self,symbol,date,price):
        filename = symbol + ".trade"
        
        try:
            with open(filename,"r") as fobj:
                content = json.load(fobj)
                fobj.close()
        except:
            dictFMT = {"Stats" : {},"BUY" : {}, "SELL" : {}}
            with open(filename,"w") as fobj:
                json.dump(dictFMT,fobj,indent=6)
                fobj.close()
            with open(filename,"r") as fobj:
                content = json.load(fobj)
                fobj.close()

        content["SELL"][date] = round(price,2)

        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()      

    def momsqzevol(self,symbol):
        startTime = time.time()
        S = strategy()
        filename = symbol + ".csv"
        dataF = pd.read_csv(filename)
        buyCount = 0 # to ensure sell only when the stock is in holdings
        iterVar = 51
        while True:
            try:
                if (dataF["vol_avg"].iloc[iterVar] > dataF["Volume"].iloc[iterVar - 1]) and (dataF["MOMSQZE"].iloc[iterVar] == "TRNDu"):
                    S.simulateBuy(symbol,dataF["Date"].iloc[iterVar],dataF["Close"].iloc[iterVar])
                    buyCount += 1
                if (dataF["Close"].iloc[iterVar] < dataF["10_ma"].iloc[iterVar - 1]) and (buyCount > 0):
                    S.simulateSell(symbol,dataF["Date"].iloc[iterVar],dataF["Close"].iloc[iterVar])
                    buyCount -= 1
                iterVar += 1
            except:
                endTime = time.time()
                print(f"[OK] completed strategy test for {symbol} in {round(endTime - startTime,2)} second(s)")
                break

    def momsqzevolTUPLES(self,symbol):
        startTime = time.time()
        S = strategy()
        filename = symbol + ".csv"
        dataF = pd.read_csv(filename)
        buyCount = 0 # to ensure sell only when the stock is in holdings
        # dataF = dataF.iloc[50:]
        
        for i in dataF.itertuples():
            prevIndex = int(i.Index) - 1
            if not math.isnan(i.vol_avg):
                if i.MOMSQZE == "TRNDu":
                    if i.vol_avg > dataF["Volume"].iloc[prevIndex]:
                        S.simulateBuy(symbol,i.Date,i.Close)
                        buyCount += 1
                elif i._17 < dataF["Close"].iloc[prevIndex]:
                    if buyCount >= 1:
                        S.simulateSell(symbol,i.Date,i.Close)
                        buyCount -= 1
        
        endTime = time.time()
        print(f"[OK] completed strategy test for {symbol} in {round(endTime - startTime,2)} second(s)")



    def runStats(self,symbol):
        
        startTime = time.time()

        S = strategy()
        filename = symbol + ".trade"
        
        with open(filename,"r") as fobj:
            content = json.load(fobj)
            fobj.close()

        totalBuy = S.totalBuyCost(content) # Total cost for BUY opportunities
        countBuy  = S.totalBuyCost(content,count=True) # Count of opportunities
        countSell  = S.totalSellCost(content,count=True) # Count of opportunities
        totalSell = S.totalSellCost(content) # Total cost for SELL opportunities
        P_L = round(totalSell - totalBuy,2) # Profit and Loss
        P_L_percen = round(((P_L / totalBuy) * 100), 2) # Profit and Loss percentage
        totalTrades = S.totalTrades(totalBuy,totalSell) # Total number of trades made
        netTrades = S.netTrades(countBuy, countSell) # Net trades


        content["Stats"]["Total Buy"] = totalBuy
        content["Stats"]["Total Sell"] = totalSell
        content["Stats"]["P/L"] = P_L
        content["Stats"]["P/L percentage"] = P_L_percen
        content["Stats"]["Buy opportunities"] = countBuy
        content["Stats"]["Sell opportunities"] = countSell
        content["Stats"]["Total trades"] = totalTrades
        content["Stats"]["Net trades"] = netTrades


        with open(filename,"w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()

        endTime = time.time()
        print(f"[OK] completed stats for {symbol} in {round(endTime - startTime,2)} second(s)")

    def totalBuyCost(self,dataF,count=False):
        
        buyData = dataF["BUY"].values()
        cnt = len(dataF["BUY"].keys())
        sum = 0.0
        
        for i in buyData:
            sum += i

        sum = round(sum,2)

        if not count:
            return sum
        else:
            return cnt

    def totalSellCost(self,dataF,count=False):
        
        sellData = dataF["SELL"].values()
        cnt = len(dataF["SELL"].keys())
        sum = 0.0
        
        for i in sellData:
            sum += i

        sum = round(sum,2)

        if not count:
            return sum
        else:
            return cnt

    def totalTrades(self,buy,sell):
        tot =  buy + sell
        return tot
       
    def netTrades(self,buy,sell):
        net = buy - sell
        if net < 0:
            raise ValueError ("net trades cannot be negative")
        return net


        
def gatherData():
    T = technical()
    scrips = method.loadScrips()

    for i in scrips:   
        dataF = method.getData(i)
        T.get_keltner_bands(i,dataF)
        T.get_bollinger_bands(i,dataF)
        T.get_momentum_squeeze(i,dataF)
        T.get_avg_volume(i,dataF)
        T.get_10day_ma(i,dataF)
        print(f"[OK] writing data to csv for {i}")
        method.dumpData(i,dataF)

def test():
    S = strategy()
    scrips = method.loadScrips()
    for j in scrips:
        S.momsqzevolTUPLES(j) # replace the method here for different backtest strategies
        S.runStats(j)

def main():
    print("1. Gather data")
    print("2. Test strategy")
    ch = int(input("enter choice : "))
    if ch == 1:
        gatherData()
    elif ch == 2:
        test()
    else:
        raise ValueError ("invalud input")
    


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"completed execution in {round(end-start,2)} second(s)")