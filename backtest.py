### Currently only testing NSE

from datetime import date, datetime
from datetime import datetime
import datetime
import json
import math



hotli = []
sellli = []

with open("settings.json","r") as fobj:
    content = json.load(fobj)
    fobj.close()

showTrades = content["showTrades"]

def remComma(string):
    modStr = ""
    for i in string:
        if i != ",":
            modStr += i
        else:
            pass
    return modStr

def selloff():
    
    with open("selloff.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    print()
    now = datetime.datetime.now()
    todayDate = now.strftime("%d/%m/%Y")
    todayDate = str(todayDate)
    print("---SELL OFF---",todayDate)
    for i in sellli:
        print(i)

    content[todayDate] = sellli

    with open("selloff.json","w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()

def hotlist():

    with open("hotlist.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    with open("redflags.json","r") as fobj:
        flags = json.load(fobj)
        fobj.close()

    redflags = []

    flagsli = list(flags.values())
    try:
        for i in flagsli:
            redflags.extend(i)
    except:
        pass

    print()
    now = datetime.datetime.now()
    todayDate = now.strftime("%d/%m/%Y")
    todayDate = str(todayDate)
    print("---HOT LIST---",todayDate)
    try:
        if hotli == []:
            raise ValueError ("Hot list is empty")
        else:
            for i in hotli:
                if i not in redflags:
                    print(i)
                else:
                    if showRedFlags:
                        print(i)
    except ValueError:
        print("Hotlist is empty")

    content[todayDate] = hotli

    with open("hotlist.json","w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()

def main(company):

    filename = company + ".json"

    with open(filename,"r") as fobj:
        content = json.load(fobj)

    try:
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
        tenMA = content["Technical Indicators"]["10 day MA"]
    except Exception:
        raise ValueError (f"corrupt or incomplete data for {company}")

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
    
    # dealing with NaN params
    rsiNaN, adxNaN, macdlNaN, macdsNaN, MFINaN = False, False, False, False, False
    if math.isnan(rsi):
        rsiNaN = True
    elif math.isnan(adx):
        adxNaN = True
    elif math.isnan(macdl):
        macdlNaN = True
    elif math.isnan(macds):
        macdsNaN = True
    elif math.isnan(mfi):
        MFINaN = True
    else:
        pass

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

    with open("params.json","r") as fobj:
        buyParams = json.load(fobj)
        fobj.close()

    if (macdl > 0.0 and macds > 0.0) and (macds > macdl):
        macdInd = True

    if changePercen > buyParams["buy"]["change percen"]:
        changeInd = True

    if float(currentPrice_mod) > float(fiftyTwoWeekLow_mod):
        fiftyTwoWeekInd = True

    if authDeliv:
        if delivPercen > buyParams["buy"]["deliv percen"]:
            delivInd = True

    if fiftyDayVol:
        fiftyDayVolInd = True

    if momsqze == "TRNDu":
        momsqzeInd = True

    if rsi <= buyParams["buy"]["rsi value"]: 
        rsiInd = True

    if adx > buyParams["buy"]["adx value"]:
        adxInd = True

    if mfi < buyParams["buy"]["mfi value"]:
        mfiInd = True

    # [BUY] Weighted Indicator Decision 

    if (delivInd or fiftyDayVolInd):
        toBUY = True

    if ((fiftyTwoWeekInd) and (rsiInd and adxInd and macdInd and mfiInd) and (momsqzeInd) or fiftyDayVolInd):
        toBUY = True
    else:
        toBUY = False

    # Check for NaN values (NaN values result in auto reject BUY)

    if rsiNaN or adxNaN or macdlNaN or macdsNaN or MFINaN:
        toBUY = False

    # Hotlist 

    if fiftyDayVolInd and momsqzeInd:
        hotli.append(symbol)

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

    with open("params.json","r") as fobj:
        sellParams = json.load(fobj)
        fobj.close()

    if (macdl < 0.0 and macds < 0.0) and (macds < macdl):
        macdInd = True

    if changePercen < sellParams["sell"]["change percen"]:
        changeInd = True

    if float(currentPrice_mod) < float(fiftyTwoWeekLow_mod):
        fiftyTwoWeekInd = True

    if authDeliv:
        if delivPercen > sellParams["sell"]["deliv percen"]:
            delivInd = True

    if fiftyDayVol:
        fiftyDayVolInd = True

    if momsqze == "TRNDd":
        momsqzeInd = True

    if rsi > sellParams["sell"]["rsi value"]:
        rsiInd = True

    if adx > sellParams["sell"]["adx value"]:
        adxInd = True

    if mfi > sellParams["sell"]["mfi value"]:
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

    # Sell off
    cp = remComma(currentPrice)
    if float(cp) < float(tenMA):
        sellli.append(symbol)

    # Updating trades.json file

    if toBUY:
        if not onlySell:
            if showTrades:
                print(f"+ BUYING {symbol} STOCK")
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
        if not onlyBuy:
            if showTrades:
                print(f"- SELLING {symbol} STOCK")
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

            if symbol not in content: # we do not have that stock in our portfolio
                pass
            else:
                content[symbol].extend(dumper)

            with open("trades.json","w") as fobj:
                json.dump(content,fobj,indent=6)
                fobj.close()

with open("settings.json","r") as fobj:
    settings = json.load(fobj)
    ovrwrt = settings["ovrwrt"]
    onlyBuy = settings["onlyBuy"]
    onlySell = settings["onlySell"]
    showRedFlags = settings["showFlagsHotlist"]

with open("NSE.json","r") as fobj:
    NSE = json.load(fobj)
    fobj.close()

for company in NSE:
    main(company)

selloff()
hotlist()