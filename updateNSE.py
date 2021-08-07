import pandas as pd
import json

""" To update the NSE.json simply download the nifty50 csv file from the official NSE website """

data = pd.read_csv("ind_nifty50list.csv")
newNSE = data["Symbol"]

fmtNSE = []

# '&' => '_'

for i in newNSE:
    fmt = i + ".NS"
    fmtNSE.append(fmt)

print(fmtNSE)

with open("NSE.json","w") as fobj:
    json.dump(fmtNSE,fobj,indent=6)
    fobj.close()

