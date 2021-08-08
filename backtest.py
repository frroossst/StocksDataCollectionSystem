### Currently only testing NSE

from datetime import date, datetime
import datetime
import json

def remComma(string):
    modStr = ""
    for i in string:
        if i != ",":
            modStr += i
        else:
            pass
    return modStr

def main(company):
    
    # Only accounts for Saturdays and Sundays not for other festive holidays
    if not ovrwrt:
        weekDay = datetime.datetime.today().weekday()
        if weekDay == 5 or weekDay == 6:
            print("The markets remain closed on weekends")
            quit()

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
    macdl = content["Technical Indicators"]["MACD"][0]["Line"]
    macds = content["Technical Indicators"]["MACD"][1]["Signal"]
    fiftyDayVol = content["Technical Indicators"]["50 day volume trend"]
    momsqze = content["Technical Indicators"]["MOMSQZE"]
    mfi = content["Technical Indicators"]["MFI"]

    # Manipulating data
    changePercen = changePercen[:-1]
    changePercen = float(changePercen)
    if delivPercen != "NA":
        delivPercen = delivPercen[:-1]
        delivPercen = float(delivPercen)
        authDeliv = True
    else:
        authDeliv = False

    currentPrice_mod = remComma(currentPrice)
    fiftyTwoWeekLow_mod = remComma(fiftyTwoWeekLow)
    
    # [BUY] Setup

    changeInd = False
    fiftyTwoWeekInd = False
    delivInd = False
    fiftyDayVolInd = False
    momsqzeInd = False
    rsiInd = False
    adxInd = False
    macdInd = False
    mfiInd = False

    if (macdl > 0.0 and macds > 0.0) and (macds > macdl) and (abs(macds - macdl) > 1):
        macdInd = True

    if changePercen > 0.0:
        changeInd = True

    if float(currentPrice_mod) > float(fiftyTwoWeekLow_mod):
        fiftyTwoWeekInd = True

    if authDeliv:
        if delivPercen > 30.00:
            delivInd = True

    if fiftyDayVol:
        fiftyDayVolInd = True

    if momsqze == "TRNDu":
        momsqzeInd = True

    if rsi <= 70.00: # just for human
        rsiInd = True

    if adx > 21.00:
        adxInd = True

    if mfi < 70.00:
        mfiInd = True

    # [BUY] Weighted Indicator Decision 

    if (delivInd or fiftyDayVolInd):
        toBUY = True

    if (fiftyTwoWeekInd) and (rsiInd and adxInd and macdInd and mfiInd) and (momsqzeInd):
        toBUY = True
    else:
        toBUY = False

    # [SELL] Setup

    changeInd = False
    fiftyTwoWeekInd = False
    delivInd = False
    fiftyDayVolInd = False
    momsqzeInd = False
    rsiInd = False
    adxInd = False
    macdInd = False
    mfiInd = False

    if macdl < 0.0 and macds < 0.0:
        macdInd = True

    if changePercen < -5.00:
        changeInd = True

    if float(currentPrice_mod) < float(fiftyTwoWeekLow_mod):
        fiftyTwoWeekInd = True

    if authDeliv:
        if delivPercen > 30.00:
            delivInd = True

    if fiftyDayVol:
        fiftyDayVolInd = True

    if momsqze == "TRNDd":
        momsqzeInd = True

    if rsi > 75.00:
        rsiInd = True

    if adx > 21.00:
        adxInd = True

    if mfi > 80.00:
        mfiInd = True

    # [SELL] Weighted Indicator Decision 

    sureSELL = False
    profitSELL = False
    toSELL = False

    if macdInd:
        sureSELL = True
    if rsiInd:
        sureSELL = True
    if changeInd:
        sureSELL = True
    if fiftyTwoWeekInd:
        sureSELL = True
    if mfiInd:
        sureSELL = True

    if (rsiInd) or (momsqzeInd and adx):
        profitSELL = True

    if sureSELL:
        toSELL = True
    elif profitSELL:
        toSELL = True
    else:
        toSELL = False

    # Updating trades.json file

    if toBUY:
        print(f"BUYING {symbol} STOCK")
        with open("trades.json","r") as fobj:
            content = json.load(fobj)
            fobj.close()

        dateB = date.today()
        dateB = dateB.strftime("%d/%m/%Y")

        qtyB = 1
        priceB = currentPrice_mod

        dumper = ("BUY","ENTRY",dateB,qtyB,priceB)

        if symbol not in content:
            content[symbol] = dumper 

        else:
            if content[symbol][2] == str(dateB):
                pass
            else:
                content[symbol].extend(dumper)

        with open("trades.json","w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()

    if toSELL:
        print(f"SELLING {symbol} STOCK")
        with open("trades.json","r") as fobj:
            content = json.load(fobj)
            fobj.close()

        dateB = date.today()
        dateB = dateB.strftime("%d/%m/%Y")
        qtyB = 1
        priceB = currentPrice_mod

        if sureSELL:
            dumper = ("SELL","EXIT",dateB,qtyB,priceB,)
        else:
            dumper = ("SELL","BOOK",dateB,qtyB,priceB)

        if symbol not in content:
            content[symbol] = dumper 

        else:
            if content[symbol][2] == str(dateB):
                pass
            else:
                content[symbol].extend(dumper)

        with open("trades.json","w") as fobj:
            json.dump(content,fobj,indent=6)
            fobj.close()



toBUY = False
ovrwrt = False
authDeliv = True

with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()

for company in NSE:
    main(company)