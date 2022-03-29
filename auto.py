from datetime import datetime
import holiday
import json
import time



def writeFlagLogs():
    with open("logs.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    todayDate = datetime.today()
    todayDate = todayDate.strftime("%d-%m-%Y")
    content[todayDate] = True

    with open("logs.json","w") as fobj:
        json.dump(content,fobj,indent=6)
        fobj.close()

def getFlagLogs() -> bool:

    todayDate = datetime.today()
    todayDate = todayDate.strftime("%d-%m-%Y")

    with open("logs.json","r") as fobj:
        content = json.load(fobj)
        fobj.close()

    try:
        isRedFlags = content[todayDate]
    except KeyError:
        isRedFlags = False

    return isRedFlags

def program():
    contVar = holiday.mainCheck()
    if contVar:
        print("[OK] markets are open")
        todayRedFlags = getFlagLogs()
        if not todayRedFlags:
            print("[OK] gathering flags")
            import flags
        print("[OK] collecting scrip data")
        import scraper
        print("[OK] running technical analysis")
        import algorithm
        print("[OK] running trading algorithm")
        import backtest
        writeFlagLogs()
    else:
        print("[ERROR] markets are closed")

def autoScript():
    start = time.time()

    try:
        program()
    except Exception as e:
        print(f"[ERROR] {e}")
        program()

    end = time.time()

    print() 
    print(f"completed execution in {round((end - start),2)} second(s)")

if __name__ == "__main__":
    DEBUG = False
    if DEBUG:
        import scraper
        import algorithm
        import backtest
    else:
        autoScript()
