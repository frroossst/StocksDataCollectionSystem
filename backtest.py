### Currently only testing NSE

from datetime import date
import json
import csv


toBUY = False

with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()

company = NSE[0]

filename = company + ".json"

with open(filename,"r") as fobj:
    content = json.load(fobj)

symbol = content["Basic Info"]["Symbol"]
currentPrice = content["Basic Info"]["Current Price"]
changePercen = content["Basic Info"]["Change Percent"]
fiftyTwoWeekLow = content["Basic Info"]["52 Week Low"]
delivPercen = content["Basic Info"]["Deliverable to Traded Quantity Percent"]
rsi = content["Technical Indicators"]["RSI"]
adx = content["Technical Indicators"]["ADX"]
fiftyDayVol = content["Technical Indicators"]["50 day volume trend"]
momsqze = content["Technical Indicators"]["MOMSQZE"]

changeInd = False
fiftyTwoWeekInd = False
delivInd = False
fiftyDayVolInd = False
momsqzeInd = False
rsiInd = False
adxInd = False

# Manipulating data
changePercen = changePercen[:-1]
changePercen = float(changePercen)
delivPercen = delivPercen[:-1]
delivPercen = float(delivPercen)

# BUY signals
# Each indicator is weighted
# If 3/4 are True => BUY

if changePercen > 0.0:
    changeInd = True

if float(currentPrice) > float(fiftyTwoWeekLow):
    fiftyTwoWeekInd = True

if delivPercen > 40.00:
    delivInd = True

if fiftyDayVol:
    fiftyDayVolInd = True

if momsqze == "TRND":
    momsqzeInd = True

if rsi < 70.00:
    rsiInd = True

if adx > 21.00:
    adxInd = True

# Weighted Indicator Final 

if (fiftyTwoWeekLow) and (rsiInd and adxInd) and (delivInd or fiftyDayVolInd) and (momsqzeInd):
    toBUY = True
else:
    toBUY = False
toBUY = True

if toBUY:
    print("BUYING THIS STOCK")
    with open("trades.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    dateB = date.today()
    dateB = dateB.strftime("%d/%m/%Y")
    qtyB = 1
    priceB = currentPrice

    dumper = ["BUY",dateB,qtyB,priceB]

    for i in content:
        if i == symbol:
            content[symbol].append(dumper)
        else:
            content[symbol] = dumper 

    with open("trades.json","w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()