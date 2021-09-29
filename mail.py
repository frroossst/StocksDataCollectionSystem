from datetime import datetime
import smtplib
import json

with open("credentials.secret","r") as fobj:
    cred = json.load(fobj)
    fobj.close()

emailId = cred["emailId"]
emailPass = cred["emailPass"]

