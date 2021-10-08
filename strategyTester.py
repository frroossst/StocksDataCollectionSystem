from datetime import datetime
import yfinance as yf
import pandas as pd
import json

def loadNSE() -> list:

    with open("NSE.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()
    
    return content

def getData(symbol):
    dataF = yf.Ticker(symbol).history(period="1y")
    print(dataF)
    for i in dataF:
        print(i)

scrips = loadNSE()
for i in scrips:
    getData(i)
    break