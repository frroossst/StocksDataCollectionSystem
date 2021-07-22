import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import selenium

# Basic Stocks Trading Strategy

# [BUY]
# 1. 26 week high is greater than 52 week high
# 2. RSI > 70 
# 3. ADX > 25
# 4. MACD signal is true
# 5. 50 day EMA is greater than 200 day EMA
# 6. OBV signal is up!

# [SELL]
# 1. 26 week average is less than 52 week high
# 2. RSI > 75
# 3. ADX > 25
# 4. MACD is set to sell
# 5. current price is 0.70 * bought price

is52weekHigh = False
isRSI = False
isADX = False
isMACD = False
is50dayEMA = False
isOBV = False                                                                

nvda = yf.Ticker("NVDA")

historical = nvda.info

currentPrice = nvda.info["regularMarketPrice"]
fiftyTwoWeekHigh = nvda.info["fiftyTwoWeekHigh"]

if currentPrice > fiftyTwoWeekHigh:
    print("Current price is greater than 52 week high")
    is52weekHigh = True
else:
    print("Current price is less than 52 week high")
    is52weekHigh = False

