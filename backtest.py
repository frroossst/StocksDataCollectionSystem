import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import time
import requests
from bs4 import BeautifulSoup


# # # Basic Stocks Trading Strategy

# # # [BUY]
# # # 1. 26 week high is greater than 52 week high
# # # 2. RSI > 70 
# # # 3. ADX > 25
# # # 4. MACD signal is true
# # # 5. 50 day EMA is greater than 200 day EMA
# # # 6. OBV signal is up!

# # # [SELL]
# # # 1. 26 week average is less than 52 week high
# # # 2. RSI > 75
# # # 3. ADX > 25
# # # 4. MACD is set to sell
# # # 5. current price is 0.70 * bought price

# BS4 method

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

url = "https://finance.yahoo.com/quote/NVDA"

r = requests.get(url)

soup = BeautifulSoup(r.text,"html.parser")

print(soup.title.text)

currentPrice = soup.find("span",{"class" : "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
print(currentPrice)










# is52weekHigh = False
# isRSI = False
# isADX = False
# isMACD = False
# is50dayEMA = False
# isOBV = False                                                                


# nvda = yf.Ticker("NVDA")
# historical = nvda.info
# currentPrice = nvda.info["regularMarketPrice"]
# fiftyTwoWeekHigh = nvda.info["fiftyTwoWeekHigh"]
# hist = nvda.history(period="max")
# hist.to_csv()
# print(hist)

# if currentPrice > fiftyTwoWeekHigh:
#     print("Current price is greater than 52 week high")
#     is52weekHigh = True
# elif currentPrice < fiftyTwoWeekHigh:
#     print("Current price is less than 52 week high")
#     is52weekHigh = False


