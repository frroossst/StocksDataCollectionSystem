import scraper
import algorithm
import backtest
import json

with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()

scraper.main(num=1,exch="NSE",auto=True)

for i in NSE:
    algorithm.main(i)

for j in NSE:
    backtest.main(j)

# backtest.hotlist()