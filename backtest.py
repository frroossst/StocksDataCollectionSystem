import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

PATH = "/home/home/Desktop/Projects/Stonks/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://in.finance.yahoo.com/")

search = driver.find_element_by_id("yfin-usr-qry")
search.send_keys("NVDA")
search.send_keys(Keys.RETURN)


time.sleep(60)

driver.quit()






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

# if currentPrice > fiftyTwoWeekHigh:
#     print("Current price is greater than 52 week high")
#     is52weekHigh = True
# elif currentPrice < fiftyTwoWeekHigh:
#     print("Current price is less than 52 week high")
#     is52weekHigh = False


